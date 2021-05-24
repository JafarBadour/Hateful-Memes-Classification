import 'package:flutter/material.dart';
import 'package:classify_ateful_memes/loading.dart';
import 'package:classify_ateful_memes/loading_first.dart';
import 'package:classify_ateful_memes/classifier.dart';
import 'package:classify_ateful_memes/consent.dart';

void main() => runApp(MaterialApp(
    initialRoute: '/',
    routes: {
      '/': (context) => Loading_first(),
      '/loading': (context) => Loading(),
      '/consent' : (context) => Consent(),
      '/home': (context) => Classifier(),
    }
));