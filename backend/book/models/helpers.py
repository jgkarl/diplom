from django.contrib.auth import get_user_model

def snake_to_sentence(snake_str):
    # Split the string by underscores
    words = snake_str.split('_')
    # Capitalize the first letter of each word
    capitalized_words = [word.capitalize() for word in words]
    # Join the words with spaces to form a sentence
    sentence_case_str = ' '.join(capitalized_words)
    return sentence_case_str

# Example usage
# input_str = "this_is_a_test_string"
# print(snake_to_sentence(input_str))  # Output: "This Is A Test String"

def get_superuser():
    User = get_user_model()
    superuser = User.objects.filter(is_superuser=True).first()
    return superuser