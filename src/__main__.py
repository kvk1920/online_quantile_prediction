import sys


COMMON_HELP = 'python3 -m src run ficnn'


if '__main__' == __name__:
    if len(sys.argv) <= 1:
        print("invalid usage!")
        print(COMMON_HELP)
        exit(0)
    if 'run' == sys.argv[1]:
        from . import run_experiment
        run_experiment.run(sys.argv[2:])
    if 'visualize' == sys.argv[1]:
        from . import visualize_result
        if 'quantiles' == sys.argv[2]:
            visualize_result.show_quantiles(sys.argv[3:])
        elif 'crps' == sys.argv[2]:
            visualize_result.show_crps(sys.argv[3:])
