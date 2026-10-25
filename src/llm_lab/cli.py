import argparse,logging,os,sys
from .logging_setup import config_logging
from .providers import get_provider
from .providers.base import ProviderError

logger = logging.getLogger("llm_lab.cli")

def build_msg(question: str):
    return [
        {"role": "system", "content": "You are a helpful assistant. Answer Briefly."},
        {"role": "user", "content": question},
    ]


def main(argv=None) -> int:
    config_logging()
    parser = argparse.ArgumentParser(description="llm-lab")
    parser.add_argument(
        "question", nargs="?", help="The question to ask the LLM"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=os.environ.get("LLM_PROVIDER", "mock"),
        help="The provider to use",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("LLM_TIMEOUT", "30")),
        help="The timeout in seconds for the request, defaults to 30 seconds",
    )
    args = parser.parse_args(argv)
    
    if not args.question or not args.question.strip():
        parser.print_usage(sys.stderr)
        print("Error: A question is required", file=sys.stderr)
        return 2
    

    try:
        provider = get_provider(args.provider)
    except ProviderError as e:
        print(f"Error: {e}", file=sys.stderr)
        #2 = usage error (bad args)
        return 2
    
    logger.info("request.start provider=%s timeout=%s", provider.name, args.timeout)

    try:
        answer = provider.complete(build_msg(args.question), timeout=args.timeout)
    except ProviderError as e:
        #never log LLM_API_KEY, req auth headers, full request body containing user text,
        #full request/response body, full tracebacks and env dumps
        logger.error("request.failure provider=%s error=%s", provider.name, e)
        print(f"Error: {e}", file=sys.stderr)
        #1 = runtime/provider error
        return 1

    #SAFE TO LOG:
    # -provider name
    # -model name
    # -chars in response
    # -elapsed time ms
    # -error type message
    # -event names req.start, req.complete, req.failure
    # -truncated error messages
    logger.info("request.complete provider=%s chars=%d", provider.name, len(answer.content))
    print(answer.content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
