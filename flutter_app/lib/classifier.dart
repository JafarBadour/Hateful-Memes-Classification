import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_tindercard/flutter_tindercard.dart';
import 'dart:math';
import 'dart:core';
import 'package:http/http.dart' as http;
import 'package:pie_chart/pie_chart.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Classifier(),
    );
  }
}

class Classifier extends StatefulWidget {
  @override
  _ClassifierState createState() => _ClassifierState();
}

class _ClassifierState extends State<Classifier> with TickerProviderStateMixin {
  Map data = {};
  double a_total = 0;
  double b_total = 0;
  double a_profile = 0;
  double b_profile = 0;
  Map<String, double> stats;

  Future<void> checkfornewupadtes() async {
    String baseurl = 'http://18.221.173.110:5555/';
    print("IN checkfornewupadtes");
    final response = await http.get(baseurl + 'stats'); //+data["id"]);
    print(response.body);
    var as = response.body.split("/");
    a_total = double.parse(as[0]);
    b_total = double.parse(as[1]);

    final response2 =
        await http.get(baseurl + 'stats/' + data["id"]); //+data["id"]);
    print(response2.body);
    as = response2.body.split("/");
    a_profile = double.parse(as[0]);
    b_profile = double.parse(as[1]);

    // print(a_total + "  " + b_total);
    // print(a_profile + "  " + b_profile);

    setState(() {});
  }

  Timer timer;

  @override
  void initState() {
    super.initState();
  }

  void skip() async {
    CardController controller = data["controller"];
    data['temp'] = "2";
    controller.triggerRight();
  }

  var counter = 0;
  var profile;
  var urls;
  var first_build = true;
  CardController controller;

  Map<String, double> get_stats_profile() {
    return {
      "Hateful labeled :: ${data["id"]}": a_profile,
      "Benign labeled :: ${data["id"]}": b_profile
    };
  }

  Map<String, double> get_stats_all() {
    return {
      "Hateful": a_total,
      "Benign/not meme": b_total
    };
  }

  @override
  Widget build(BuildContext context) {
    print('Building classifier');
    if (first_build) {
      data = ModalRoute.of(context).settings.arguments;

      timer = Timer.periodic(
          Duration(seconds: 30), (Timer t) => checkfornewupadtes());
      urls = data['urls'];
      profile = data["id"];
      for (var i = 0; i < urls.length; i++) {
        urls[i] = urls[i];
      }
      controller = CardController(); //Use this to trigger swap.

      data["controller"] = controller;
      first_build = false;
    }
    String text = "";
    double _euclidean = 0;

    var zbr = Colors.black.withOpacity(0.1);
    return new Scaffold(
      appBar: AppBar(
        title: Text('Classify Hateful Memes, profile id: ' + data["id"]),
      ),
      body: new Center(
        child: Column(children: [
          Container(
            height : MediaQuery.of(context).size.height * 0.15,
              child: PieChart(dataMap: get_stats_profile()),
          ),
          Container(
              height: MediaQuery.of(context).size.height * 0.05,
              color: Colors.white,
              child:
                  ElevatedButton(onPressed: skip, child: Text("Not a meme"))),
          Container(
            height: MediaQuery.of(context).size.height * 0.6,
            child: new TinderSwapCard(
              swipeUp: true,
              swipeDown: true,
              orientation: AmassOrientation.BOTTOM,
              totalNum: urls.length,
              stackNum: 3,
              swipeEdge: 4.0,
              maxWidth: MediaQuery.of(context).size.width * 0.8,
              maxHeight: MediaQuery.of(context).size.width * 0.8,
              minWidth: MediaQuery.of(context).size.width * 0.4,
              minHeight: MediaQuery.of(context).size.width * 0.4,
              cardBuilder: (context, index) => Card(
                child: Stack(children: <Widget>[
                  ColorFiltered(
                    colorFilter: ColorFilter.mode(zbr, BlendMode.dstOver),
                    child: Image.network('${urls[index]}/${profile}',
                        fit: BoxFit.fill),
                  ),
                  Align(
                      alignment: Alignment.bottomCenter,
                      child: Text(
                        text,
                        style: TextStyle(height: 10, fontSize: 22),
                      )),
                ]),
              ),
              cardController: controller = controller,
              swipeUpdateCallback:
                  (DragUpdateDetails details, Alignment align) {
                /// Get swiping card's alignment

                _euclidean = min(10, align.x.abs() + align.y.abs()) / 30.0;

                if (align.x < -0.5) {
                  //Card is LEFT swiping
                  zbr = Colors.red.withOpacity(1.0 - _euclidean);
                  text = "Hateful";
                } else if (align.x > 0.5) {
                  //Card is RIGHT swiping
                  text = "Not Hateful";
                  zbr = Colors.blue.withOpacity(1.0 - _euclidean);
                } else {
                  zbr = Colors.black.withOpacity(0.1);
                }
              },
              swipeCompleteCallback:
                  (CardSwipeOrientation orientation, int index) {
                counter += 1;
                zbr = Colors.black.withOpacity(0.1);
                var s = urls[index];

                var ind = s.indexOf('src/');
                var path = s.substring(ind + 4, s.length);
                print(path);
                //print(orientation);
                //  print(urls[index]);
                // print(path);
                String baseurl = 'http://18.221.173.110:5555/';
                var label = '0';
                if (orientation == CardSwipeOrientation.LEFT) {
                  label = '1';
                  a_profile += 1;
                  a_total += 1;
                } else {
                  b_total += 1;
                  b_profile += 1;
                }
                if (data['temp'] == "2") label = "2";

                data['temp'] = 0;
                print(label);
                var profile = data["id"];
                print("profile" +
                    " " +
                    data["id"] +
                    "counter: " +
                    counter.toString());
                print(
                    baseurl + 'classify/' + path + '/' + label + "/" + profile);
                final response = http.get(
                    baseurl + 'classify/' + path + '/' + label + "/" + profile);
                //print(response);
                // print(baseurl+'classify/'+path+'/'+label);

                /// Get orientation & index of swiped card
                setState(() {});
              },
            ),
          )
        ]),
      ),
    );
  }
}
