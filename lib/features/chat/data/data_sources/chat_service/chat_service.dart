// import 'dart:convert';
// import 'dart:developer';

// import 'package:web_socket_client/web_socket_client.dart';

// class ChatService {
//   static final _instance = ChatService._internal();
//   WebSocket? _socket;

//   factory ChatService() => _instance;
//   ChatService._internal();

//   void connect() {
//     _socket = WebSocket(Uri.parse("ws://localhost:8000/ws/chat"));

//     _socket!.messages.listen((onData) {
//       final data = jsonDecode(onData);
//       log(data);
//     });
//   }

//   void chat(String query) {
//     _socket!.send({"query": query});
//   }
// }

import 'dart:convert';
import 'dart:developer';
import 'package:web_socket_client/web_socket_client.dart';

class ChatService {
  static final _instance = ChatService._internal();
  WebSocket? socket;

  factory ChatService() => _instance;
  ChatService._internal();

  void connect() {
    final uri = Uri.parse("ws://localhost:8000/ws/chat");
    socket = WebSocket(uri);

    socket!.messages.listen((data) {
      log("Received: $data");
    });

    socket!.connection.listen(
      (state) => log("Socket state: $state"),
      onError: (e) => log("Socket error: $e"),
    );
  }

  void chat(String query) {
    if (socket != null && socket!.connection.state is Connected) {
      final payload = jsonEncode({"query": query});
      socket!.send(payload);
    } else {
      log("Socket not connected");
    }
  }

  void close() {
    socket?.close();
  }
}
