import 'package:api/api.dart' as api;

void main(List<String> arguments) async {
  
  String? question = await api.getQuestionText();
  bool? answer = await api.getCorrectAnswer();

  print('Question: $question');
  print('Answer: $answer');
}
