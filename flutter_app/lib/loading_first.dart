import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:async';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class Loading_first extends StatefulWidget {
  @override
  _LoadingState createState() => _LoadingState();
}

class _LoadingState extends State<Loading_first> {
  Map data = {};
  void get_urls() async {
    //18.221.173.110
    await Future.delayed(Duration(seconds: 2));
    Navigator.pushReplacementNamed(context, '/consent', arguments: {

    });
  }

  @override
  void initState() {
    super.initState();
    get_urls();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.blue[900],
        body: Center(
            child: SpinKitFadingCube(
              color: Colors.white,
              size: 50.0,
            )
        )
    );
  }
}