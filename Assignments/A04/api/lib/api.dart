import 'package:http/http.dart' as http;
import 'dart:convert' as convert;

//TODO Make QuizBrain using http requests

Future<void> nextQuestion() async {
  Uri url = Uri.http('localhost:8888', '/question');

  // Await the http get response, then decode the json-formatted response.
  var response = await http.get(url);
}

Future<String?> getQuestionText() async {
  Uri url = Uri.http('localhost:8888', '/question');

  // Await the http get response, then decode the json-formatted response.
  var response = await http.get(url);
  if (response.statusCode == 200) {
    var jsonResponse =
        convert.jsonDecode(response.body) as Map<String, dynamic>;
    String question = jsonResponse['question'];
    return question;
  }
  return null;
}

Future<bool?> getCorrectAnswer() async {
  Uri url = Uri.http('localhost:8888', '/answer');

  // Await the http get response, then decode the json-formatted response.
  var response = await http.get(url);
  if (response.statusCode == 200) {
    var jsonResponse =
        convert.jsonDecode(response.body) as Map<String, dynamic>;
    bool answer = jsonResponse['answer'];
    return answer;
  }
  return null;
}

//TODO Fix this, returns null instead of false
Future<bool?> isFinished() async {
  Uri url = Uri.http('localhost:8888', '/finished');

  // Await the http get response, then decode the json-formatted response.
  var response = await http.get(url);
  if (response.statusCode == 200) {
    var jsonResponse =
        convert.jsonDecode(response.body) as Map<String, dynamic>;
    bool isFinished = jsonResponse['isFinished'];
    return isFinished;
  }
  return null;
}

Future<void> reset() async {}
