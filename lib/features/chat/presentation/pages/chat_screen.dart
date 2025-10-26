import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:dash_chat_2/dash_chat_2.dart';
import 'package:perplexity_clone/features/chat/data/data_sources/chat_service/chat_service.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ChatUser user = ChatUser(id: '1', firstName: 'Me');
  final ChatUser botUser = ChatUser(id: '2', firstName: 'Bot');
  final ChatService chatService = ChatService();

  List<ChatMessage> messages = [];

  @override
  void initState() {
    super.initState();
    chatService.connect();

    // Listen for backend messages
    chatService.socket?.messages.listen((rawData) {
      final data = jsonDecode(rawData);
      setState(() {
        messages.add(
          ChatMessage(
            text: data['response'] ?? data.toString(),
            user: botUser,
            createdAt: DateTime.now(),
          ),
        );
      });
    });
  }

  void sendMessage(ChatMessage message) {
    setState(() {
      messages.add(message);
    });

    // Send to backend
    chatService.chat(message.text);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Chat with Backend")),
      body: DashChat(
        messages: messages,
        onSend: sendMessage,
        currentUser: user,
      ),
    );
  }

  @override
  void dispose() {
    chatService.socket?.close();
    super.dispose();
  }
}
