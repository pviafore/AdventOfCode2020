import itertools

CARD_PUBLIC_KEY=2069194
DOOR_PUBLIC_KEY=16426071

def get_loop_size(target, subject_number) -> int:
    candidate = 1
    for loop_size in itertools.count(1):
        candidate = (candidate * subject_number ) % 20201227
        if candidate == target:
            return loop_size

    raise RuntimeError("Should not ever hit here")

def get_encryption_key(card_public_key, door_public_key) -> int:
    card_loop_size = get_loop_size(card_public_key, 7)
    subject_number = door_public_key
    candidate = 1
    for _ in range(card_loop_size):
        candidate = (candidate * subject_number ) % 20201227
    return candidate



if __name__ == "__main__":
    print(get_encryption_key(CARD_PUBLIC_KEY, DOOR_PUBLIC_KEY))
