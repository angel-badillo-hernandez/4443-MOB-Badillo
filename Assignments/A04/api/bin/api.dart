/// Author: Angel Badillo Hernandez
/// 
/// Github: @It-Is-Legend27
/// 
/// Description:
/// 
/// This is an example of how to use the API.
import 'package:api/api.dart' as api;

/// Prints all the questions and answers in the api
void main(List<String> arguments) async {
  // Ensure ID is at 0
  api.reset();

  // Once the id is 1 past the last question, stop.
  // If we print past the last, the question text will be ''
  // and the answer will be false
  while (!await api.isFinished()) {
    // Get question and answer
    String question = await api.getQuestionText();
    bool answer = await api.getCorrectAnswer();

    // Print answer and question
    print('Question: $question');
    print('Answer: $answer');
    api.nextQuestion();
  }
  print('We reached the end of the questions.');

  // We went past the amount of questions
  print(await api.getQuestionText());
  print(await api.getCorrectAnswer());
}
