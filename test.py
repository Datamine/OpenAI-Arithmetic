from openai import OpenAI
from random import randint, choice
from typing import Tuple
from sympy import primefactors

client = OpenAI()
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127]


def random():
    # this is in a helper function so we can change it up as necessary
    # return choice(primes)
    # return randint(1, 100)
    return randint(812300, 812400)


def generate_arithmetic_string(operator: str, length: int) -> Tuple[str, int]:
    # initialize with one integer
    ret = f'{random()}'

    for _ in range(length - 1):
        ret += f' {operator} {random()}'

    return ret, eval(ret)


def create_completion(arithmetic_string: str):
    return client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {
                "role": "system", "content":
                """
                You are performing basic arithmetic. The user will supply an arithmetic problem.
                You are to return exactly only the solution to the problem, and nothing else.
                DO NOT return scientific notation or use commas. Return integers only.
                """
            },
            {
                "role": "user",
                "content": arithmetic_string
            }
        ]
    )


def experiment(operator, upper_limit, repetitions):
    with open(f"results_{operator}_{upper_limit}_812300.csv", "w") as f:
        f.write("Operator,Sequence Length,Repetition Number,Sequence,True Value,GPT-4 Value,\n")

        for sequence_length in range(2, upper_limit):
            # logging for me to monitor
            print("Sequence Length:", sequence_length)

            for repetition in range(repetitions):
                sequence_string, true_value = generate_arithmetic_string(operator, sequence_length)
                try:
                    completion = int(create_completion(sequence_string).choices[0].message.content.strip())
                    f.write(f"{operator},{sequence_length},{repetition},{sequence_string},{true_value},{completion},\n")
                except Exception as e:
                    print("Failure!", e)


def experiment_primes():
    for _ in range(40):
        prime_sequence = [random() for _ in range(20)]
        sequence_string = ' * '.join(str(x) for x in prime_sequence)
        true_value = eval(sequence_string)

        try:
            completion = int(create_completion(sequence_string).choices[0].message.content.strip())
            completion_factorization = primefactors(completion)
            print(completion, true_value, completion == true_value)
            print(sorted(prime_sequence))
            print(completion_factorization)
            print("")
        except Exception as e:
            print("Failure!", e)


experiment("+", 25, 20)