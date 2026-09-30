from collections import deque

class AhoCorasick:
    def __init__(self):
        # Each node contains:
        # next -> dictionary of transitions
        # fail -> failure link
        # output -> whether a banned word ends here
        self.next = [{}]
        self.fail = [0]
        self.output = [False]

    def add_word(self, word):
        node = 0

        for ch in word.lower():
            if ch not in self.next[node]:
                self.next[node][ch] = len(self.next)

                self.next.append({})
                self.fail.append(0)
                self.output.append(False)

            node = self.next[node][ch]

        self.output[node] = True

    def build(self):
        queue = deque()

        # Initialize failure links for root children
        for ch, child in self.next[0].items():
            self.fail[child] = 0
            queue.append(child)

        while queue:
            current = queue.popleft()

            for ch, child in self.next[current].items():
                queue.append(child)

                failure = self.fail[current]

                while failure != 0 and ch not in self.next[failure]:
                    failure = self.fail[failure]

                if ch in self.next[failure]:
                    self.fail[child] = self.next[failure][ch]
                else:
                    self.fail[child] = 0

                # If a banned word ends at the failure node,
                # then this node also represents a match.
                self.output[child] = (
                    self.output[child] or
                    self.output[self.fail[child]]
                )

    def contains_banned_word(self, text):
        node = 0

        for ch in text.lower():
            while node != 0 and ch not in self.next[node]:
                node = self.fail[node]

            if ch in self.next[node]:
                node = self.next[node][ch]
            else:
                node = 0

            if self.output[node]:
                return True

        return False


def has_required_pattern(password):
    """Check lowercase, uppercase, digit and allowed special symbol."""
    
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False

    for ch in password:
        if ch.islower():
            has_lower = True
        elif ch.isupper():
            has_upper = True
        elif ch.isdigit():
            has_digit = True
        elif ch in "$#@":
            has_special = True

    return has_lower and has_upper and has_digit and has_special


def has_repeated_character(password):
    """Return True if any character occurs more than 3 times consecutively."""

    if not password:
        return False

    count = 1

    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            count += 1

            if count > 3:
                return True
        else:
            count = 1

    return False


def classify_password(password, automaton):
    # Check length first
    if len(password) < 6 or len(password) > 12:
        return "WEAK_LENGTH"

    # Check banned words
    if automaton.contains_banned_word(password):
        return "COMPROMISED"

    # Check repeated characters
    if has_repeated_character(password):
        return "WEAK_PATTERN"

    # Check lowercase, uppercase, digit and special symbol
    if not has_required_pattern(password):
        return "WEAK_PATTERN"

    return "STRONG"


def main():
    # Number of banned words
    b = int(input())

    automaton = AhoCorasick()

    # Read banned words
    for _ in range(b):
        word = input().strip()

        if word:
            automaton.add_word(word)

    # Build Aho-Corasick failure links
    automaton.build()

    # Number of passwords
    n = int(input())

    # Process passwords
    for i in range(1, n + 1):
        password = input().strip()

        result = classify_password(password, automaton)

        print(f"{i}: {result}")


if __name__ == "__main__":
    main()