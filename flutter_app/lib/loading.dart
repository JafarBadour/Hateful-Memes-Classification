import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'dart:async';

class Loading extends StatefulWidget {
  @override
  _LoadingState createState() => _LoadingState();
}

class _LoadingState extends State<Loading> {
  Map data = {};
  void get_urls() async {
    //18.221.173.110
    await Future.delayed(Duration(seconds: 2));

    data = ModalRoute
        .of(context)
        .settings
        .arguments;
    String baseurl = 'http://18.221.173.110:5555/';
    var profile = data['id'];
    final response = await http.get(baseurl+'get_links/'+profile);
    var urls = response.body.split(',');
    for(int i=0;i<urls.length;i++){

      urls[i] = urls[i].replaceAll('[', '');
      urls[i] = urls[i].replaceAll(']', '');
      urls[i] = urls[i].replaceAll('\'', '');
      urls[i] = urls[i].replaceAll(' ', '');
      urls[i] = baseurl +'src/'+ urls[i];

    }
    print('url_sample '+urls[0]);
    data['urls'] = urls;
    var labeled_count = 0;
    Navigator.pushReplacementNamed(context, '/home', arguments: data);
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