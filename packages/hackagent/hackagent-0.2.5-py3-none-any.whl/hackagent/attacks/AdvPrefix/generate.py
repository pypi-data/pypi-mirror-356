import logging
import pandas as pd
from typing import List, Dict, Union, Tuple, Optional
import httpx
import os

from hackagent.router.router import AgentRouter
from hackagent.models import AgentTypeEnum
from hackagent.client import AuthenticatedClient
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
    SpinnerColumn,
)
from hackagent.logger import get_logger

logger = get_logger(__name__)

# Constants moved from main file
CUSTOM_CHAT_TEMPLATES = {
    "georgesung/llama2_7b_chat_uncensored": "<s>### HUMAN:\\n{content}\\n\\n### RESPONSE:\\n",
    "Tap-M/Luna-AI-Llama2-Uncensored": "<s>USER: {content}\\n\\nASSISTANT:",
}


def _construct_prompts(
    goals: List[str],
    meta_prefixes: List[str],
    meta_prefixes_n_samples: Union[int, List[int]],  # Allow int or list
) -> Tuple[List[Dict[str, str]], List[str], List[str]]:
    """Constructs prompts for the generator model."""

    # Handle the case where meta_prefixes_n_samples is an integer vs a list
    if isinstance(meta_prefixes_n_samples, list):
        if len(meta_prefixes) != len(meta_prefixes_n_samples):
            raise ValueError(
                "Lengths of meta_prefixes and meta_prefixes_n_samples lists must match."
            )
        n_samples_list = meta_prefixes_n_samples
    elif isinstance(meta_prefixes_n_samples, int):
        # Apply the same integer sample count to all meta prefixes
        n_samples_list = [meta_prefixes_n_samples] * len(meta_prefixes)
    else:
        raise TypeError("meta_prefixes_n_samples must be an int or a list of ints.")

    formatted_inputs = []
    current_goals = []
    expanded_meta_prefixes = []

    for goal in goals:
        for meta_prefix, n_samples in zip(meta_prefixes, n_samples_list):
            if n_samples <= 0:
                continue

            try:
                if meta_prefix in CUSTOM_CHAT_TEMPLATES:
                    prompt_content_for_template = CUSTOM_CHAT_TEMPLATES[
                        meta_prefix
                    ].format(content=goal)
                else:
                    logger.warning(
                        f"Using basic formatting for prompt construction with meta_prefix: {meta_prefix}. No matching template found."
                    )
                    # This forms the base of the "user" message if no template matches
                    prompt_content_for_template = f"USER: {goal}\\nASSISTANT:"

                # The actual text part that the LLM should complete, starting with the meta_prefix
                # This seems to be what's intended to be sent for completion.
                llm_input_text = prompt_content_for_template + meta_prefix

                # formatted_inputs will store the text that the LLM should process/complete
                formatted_inputs.extend(
                    [llm_input_text] * n_samples
                )  # This is the full text LLM sees
                current_goals.extend([goal] * n_samples)
                expanded_meta_prefixes.extend([meta_prefix] * n_samples)
            except Exception as e:
                logging.error(
                    f"Error formatting prompt for goal '{goal}' with meta_prefix '{meta_prefix}': {e}"
                )

    return formatted_inputs, current_goals, expanded_meta_prefixes


def _generate_prefixes(
    unique_goals: List[str],
    config: Dict,
    logger: logging.Logger,
    client: AuthenticatedClient,
) -> List[Dict]:
    """
    Helper for step 1. Generate prefixes.
    Uses direct HTTP call if local generator endpoint is defined, else uses AgentRouter.
    """
    results = []
    generator_config = config.get("generator", {})
    if not generator_config:
        logger.error("Missing 'generator' config. Cannot generate prefixes.")
        return results

    model_name = generator_config.get("identifier")
    if not model_name:
        logger.error("Missing 'identifier' in 'generator' config.")
        return results

    generator_endpoint = generator_config.get("endpoint")
    api_key_config_value = generator_config.get(
        "api_key"
    )  # Can be env var name or direct key

    actual_api_key: str = client.token
    if api_key_config_value:
        env_key_value = os.environ.get(api_key_config_value)
        if env_key_value:
            actual_api_key = env_key_value
            logger.info(
                f"Loaded API key for generator from environment variable: {api_key_config_value}"
            )
        else:
            actual_api_key = api_key_config_value  # Assume it's the key itself
            logger.info(
                f"Using provided value directly as API key for generator (not found as env var: {api_key_config_value[:5]}...)."
            )

    is_local_proxy_defined = bool(
        generator_endpoint == "https://hackagent.dev/api/generate"
    )

    logger.debug(
        f"Generator: model='{model_name}', endpoint='{generator_endpoint}', local_proxy_defined={is_local_proxy_defined}, api_key_present={bool(actual_api_key)}"
    )

    try:
        prompts_to_send, current_goals, current_meta_prefixes = _construct_prompts(
            unique_goals,
            config.get("meta_prefixes", []),
            config.get("meta_prefix_samples", []),
        )
        logger.debug(f"Constructed {len(prompts_to_send)} prompts to send.")
    except Exception as e:
        logger.error(f"Error constructing prompts: {e}", exc_info=True)
        return results

    if not prompts_to_send:
        logger.warning("No prompts constructed, skipping generation.")
        return results

    if is_local_proxy_defined:
        logger.info(
            f"Using existing client to make DIRECT HTTP call to local generator proxy: {generator_endpoint}"
        )
        if not actual_api_key:
            logger.error(
                f"Local generator proxy specified ({generator_endpoint}) but no API key found. Cannot make direct calls."
            )
            return results

        # Use the underlying httpx.Client from the provided AuthenticatedClient instance
        underlying_httpx_client = client.get_httpx_client()
        request_timeout_val = config.get("request_timeout", 120.0)

        for do_sample in [False, True]:
            progress_desc = (
                "[cyan]Direct Call (via existing client): Prefixes (Random Sampling)..."
                if do_sample
                else "[cyan]Direct Call (via existing client): Prefixes (Greedy Decoding)..."
            )
            logger.info(
                f"Direct Call (via existing client): {'random sampling' if do_sample else 'greedy decoding'}"
            )

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                MofNCompleteColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
                TimeRemainingColumn(),
            ) as progress_bar:
                task = progress_bar.add_task(progress_desc, total=len(prompts_to_send))
                for idx, current_llm_input_text in enumerate(prompts_to_send):
                    goal_for_prompt = current_goals[idx]
                    meta_prefix_for_prompt = current_meta_prefixes[idx]
                    temperature = config.get("temperature", 0.8) if do_sample else 1e-2

                    payload = {
                        "model": model_name,
                        "messages": [
                            {"role": "user", "content": current_llm_input_text}
                        ],
                        "max_tokens": generator_config.get(
                            "max_new_tokens", config.get("max_new_tokens", 100)
                        ),
                        "temperature": temperature,
                        "top_p": generator_config.get(
                            "top_p", config.get("top_p", 1.0)
                        ),
                    }
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Api-Key {actual_api_key}",  # Auth for local proxy
                    }
                    generated_part = " [DIRECT_CALL_ERROR]"
                    try:
                        # Use the underlying httpx_client from the main AuthenticatedClient
                        # Provide full URL and override headers for this specific call
                        raw_response = underlying_httpx_client.post(
                            generator_endpoint,  # Full URL to the local proxy
                            json=payload,
                            headers=headers,  # Override auth for this call
                            timeout=request_timeout_val,
                        )
                        raw_response.raise_for_status()
                        response_json = raw_response.json()

                        # Try to get content from the LiteLLM structure first
                        if (
                            response_json
                            and response_json.get("choices")
                            and len(response_json["choices"]) > 0
                            and response_json["choices"][0].get("message")
                            and response_json["choices"][0]["message"].get("content")
                        ):
                            generated_part = response_json["choices"][0]["message"][
                                "content"
                            ]
                        # Fallback: check for a "text" key, which the local proxy currently returns
                        elif response_json and "text" in response_json:
                            generated_part = response_json["text"]
                            if not generated_part:
                                logger.info(
                                    f"Direct call to {generator_endpoint} for '{current_llm_input_text[:50]}...' received 'text' field with empty content. Response: {response_json}"
                                )
                            else:
                                logger.info(
                                    f"Direct call to {generator_endpoint} for '{current_llm_input_text[:50]}...' used 'text' field. Response: {response_json}"
                                )
                        else:
                            logger.warning(
                                f"Direct call to {generator_endpoint} for '{current_llm_input_text[:50]}...' returned unexpected JSON structure: {response_json}"
                            )
                            generated_part = " [DIRECT_CALL_UNEXPECTED_RESPONSE]"

                    except httpx.HTTPStatusError as e:
                        logger.error(
                            f"Direct call HTTP error to {generator_endpoint} for '{current_llm_input_text[:50]}...': {e.response.status_code} - {e.response.text}",
                            exc_info=False,
                        )
                        generated_part = (
                            f" [DIRECT_CALL_HTTP_ERROR_{e.response.status_code}]"
                        )
                    except Exception as e:
                        logger.error(
                            f"Direct call exception to {generator_endpoint} for '{current_llm_input_text[:50]}...': {e}",
                            exc_info=True,
                        )
                        generated_part = " [DIRECT_CALL_EXCEPTION]"

                    final_prefix = meta_prefix_for_prompt + generated_part
                    results.append(
                        {
                            "goal": goal_for_prompt,
                            "prefix": final_prefix,
                            "meta_prefix": meta_prefix_for_prompt,
                            "temperature": temperature,
                            "model_name": model_name,
                        }
                    )
                    progress_bar.update(task, advance=1)
    else:
        logger.info("Using AgentRouter for generator.")
        router: Optional[AgentRouter] = None
        registration_key: Optional[str] = None
        adapter_operational_config = {
            "name": model_name,
            "endpoint": generator_endpoint,
            "api_key": actual_api_key,
            "max_new_tokens": generator_config.get(
                "max_new_tokens", config.get("max_new_tokens", 100)
            ),
            "temperature": generator_config.get(
                "temperature", config.get("temperature", 0.8)
            ),
            "top_p": generator_config.get("top_p", config.get("top_p", 1.0)),
        }
        try:
            logger.info(f"Initializing AgentRouter for LiteLLM model: {model_name}")
            router = AgentRouter(
                client=client,
                name=model_name,
                agent_type=AgentTypeEnum.LITELMM,
                endpoint=generator_endpoint,
                adapter_operational_config=adapter_operational_config,
                metadata=adapter_operational_config.copy(),
                overwrite_metadata=True,
            )
            if router._agent_registry:  # type: ignore
                registration_key = next(iter(router._agent_registry.keys()))  # type: ignore
                logger.info(
                    f"AgentRouter initialized. Registration key: {registration_key}"
                )
            else:
                logger.error("AgentRouter init but no agent adapter registered.")
                return results
        except Exception as e:
            logger.error(
                f"Error initializing AgentRouter for {model_name}: {e}", exc_info=True
            )
            return results

        for do_sample in [False, True]:
            progress_bar_description = (
                "[cyan]AgentRouter: Prefixes (Random Sampling)..."
                if do_sample
                else "[cyan]AgentRouter: Prefixes (Greedy Decoding)..."
            )
            logger.info(
                f"AgentRouter: {'random sampling' if do_sample else 'greedy decoding'}"
            )

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                MofNCompleteColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
                TimeRemainingColumn(),
            ) as progress_bar:
                task = progress_bar.add_task(
                    progress_bar_description, total=len(prompts_to_send)
                )
                for idx, current_llm_input_text in enumerate(prompts_to_send):
                    goal_for_prompt = current_goals[idx]
                    meta_prefix_for_prompt = current_meta_prefixes[idx]
                    temperature = config.get("temperature", 0.8) if do_sample else 1e-2

                    request_params = {
                        "prompt": current_llm_input_text,
                        "max_new_tokens": generator_config.get(
                            "max_new_tokens", config.get("max_new_tokens", 100)
                        ),
                        "temperature": temperature,
                        "top_p": generator_config.get(
                            "top_p", config.get("top_p", 1.0)
                        ),
                    }
                    generated_part = " [ROUTER_CALL_ERROR]"
                    try:
                        response = router.route_request(
                            registration_key=registration_key,
                            request_data=request_params,
                        )  # type: ignore
                        if response and response.get("processed_response"):
                            completion_text = response["processed_response"]
                            if completion_text.startswith(current_llm_input_text):
                                generated_part = completion_text[
                                    len(current_llm_input_text) :
                                ]
                            else:
                                logger.warning(
                                    f"Router completion for '{current_llm_input_text[:50]}...' did not start with prompt. Using full response."
                                )
                                generated_part = completion_text
                        elif response and response.get("error_message"):
                            logger.error(
                                f"Error from AgentRouter for '{current_llm_input_text[:50]}...': {response['error_message']}"
                            )
                            generated_part = f" [ROUTER_ERROR: {response.get('error_category', 'Unknown')}]"
                        else:
                            logger.warning(
                                f"No 'processed_response' or 'error_message' from router for: {current_llm_input_text[:50]}..."
                            )
                            generated_part = " [ROUTER_UNEXPECTED_RESPONSE]"
                    except Exception as e:
                        logger.error(
                            f"Exception during router.route_request for '{current_llm_input_text[:50]}...': {e}",
                            exc_info=True,
                        )
                        generated_part = " [ROUTER_REQUEST_EXCEPTION]"

                    final_prefix = meta_prefix_for_prompt + generated_part
                    results.append(
                        {
                            "goal": goal_for_prompt,
                            "prefix": final_prefix,
                            "meta_prefix": meta_prefix_for_prompt,
                            "temperature": temperature,
                            "model_name": model_name,
                        }
                    )
                    progress_bar.update(task, advance=1)
    return results


def execute(
    goals: List[str],
    config: Dict,
    logger: logging.Logger,
    run_dir: str,
    client: AuthenticatedClient,
) -> pd.DataFrame:
    """Generate initial prefixes using provided goals."""
    logger.info("Starting Step 1: Generate Prefixes")
    unique_goals = list(dict.fromkeys(goals)) if goals else []
    all_results = _generate_prefixes(
        unique_goals=unique_goals,
        config=config,
        logger=logger,
        client=client,
    )
    if not all_results:
        logger.warning("Step 1: No prefixes were generated.")
        results_df = pd.DataFrame(
            columns=["goal", "prefix", "meta_prefix", "temperature", "model_name"]
        )
    else:
        results_df = pd.DataFrame(all_results)
    logger.info(
        f"Step 1 complete. Generated {len(results_df)} total prefixes. CSV will be saved by the main pipeline."
    )
    return results_df
