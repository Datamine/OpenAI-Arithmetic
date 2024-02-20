from openai import OpenAI
from random import randint, choice
from typing import Tuple
from sympy import primefactors


client = OpenAI()
primes = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
    61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127
]


def random() -> int:
    """
    Set this as desired
    """
    # return choice(primes)
    # return randint(1, 100)
    # return randint(812300, 812400)
    return randint(1_158_288_283, 1_158_388_283)


def generate_arithmetic_string(operator: str, length: int) -> Tuple[str, int]:
    """
    Creates a string of the specified number of integers, interspersed with the arithmetic operator.
    Returns the true value of what that string evaluates to.
    """
    ret = f'{random()}'

    for _ in range(length - 1):
        ret += f' {operator} {random()}'

    return ret, eval(ret)


standard_prompt = (
    """
    You are performing basic arithmetic. The user will supply an arithmetic problem.
    You are to return exactly only the solution to the problem, and nothing else.
    DO NOT return scientific notation or use commas. Return integers only.
    """
)


stronger_prompt = (
    f"""
    {standard_prompt}
    Think STEP BY STEP, use only your BEST TECHNIQUES that are MOST LIKELY TO PRODUCE THE CORRECT RESULT.
    Output the correct result!
    """
)


def create_completion(arithmetic_string: str):
    return client.chat.completions.create(
        model="gpt-4-0125-preview",
        # set this as desired
        temperature=0,
        messages=[
            {
                "role": "system", "content": standard_prompt
            },
            {
                "role": "user",
                "content": arithmetic_string
            }
        ]
    )


def experiment(operator: str, upper_limit: int, repetitions: int):
    with open(f"results_{operator}_{upper_limit}.csv", "w") as f:
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


def experiment_word_problem(upper_limit: int, repetitions: int):
    with open(f"results_word_sum_{upper_limit}.csv", "w") as f:
        # semicolons since the sequence string has commas
        f.write("Sequence Length;Repetition Number;Sequence;True Value;GPT-4 Value;\n")

        for sequence_length in range(2, upper_limit):
            # logging for me to monitor
            print("Sequence Length:", sequence_length)

            for repetition in range(repetitions):
                numbers = [random() for _ in range(sequence_length)]
                true_value = sum(numbers)
                sequence_string = "Compute the sum of the following numbers: " + ", ".join([str(x) for x in numbers])
                try:
                    completion = int(create_completion(sequence_string).choices[0].message.content.strip())
                    f.write(f"{sequence_length};{repetition};{sequence_string};{true_value};{completion};\n")
                except Exception as e:
                    print("Failure!", e)


def experiment_primes():
    for _ in range(10):
        prime_sequence = [random() for _ in range(5)]
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


experiment("+", 3, 400)