import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class Consent extends StatefulWidget {
  @override
  _LoadingState createState() => _LoadingState();
}

class _LoadingState extends State<Consent> {
  Map data = {};
  var errors = "";

  void get_urls() async {
    if (data.containsKey("id"))
      Navigator.pushReplacementNamed(context, '/loading', arguments: data);
    else {
      print("NO ID");
      data["errors"] = "Press enter after writing the id to submit it";
      errors = data["errors"];
      setState(() {});
      print(get_errors());
    }
  }

  @override
  void initState() {
    super.initState();
  }

  void add_context(String s) {
    data["id"] = s;
    data["errors"] = "ID submitted: " + s;
    errors = data["errors"];
    setState(() {});
  }

  String get_errors() {
    return errors;
  }

  @override
  Widget build(BuildContext context) {
    data["errors"] = "";
    var id_submitted = false;

    return Scaffold(
        backgroundColor: Colors.redAccent[900],
        body: Center(
            child: ListView(children: [
          Container(
            padding: EdgeInsets.fromLTRB(1, 55, 1, 5),
            color: Colors.white,
            // width: 600.0,
            // height: 600.0,
            child: FittedBox(
              fit: BoxFit.contain,
              child: Column(children: [
                Text(
                    "This app contains some copyrighted material the use of which has "),
                Text(
                    "not been authorized by the author. However, we are using this material"),
                Text("to advance our research and we believe that the  "),
                Text('usage of this material is included under fair'),
                Text("use as provided in section 107 of the U.S copyright law"),
                Text("In accordance with  Title 17 of the U.S.C section 107, "),
                Text('the material on this site/app is distributed'),
                Text(
                    "without profit to those who have expressed a prior interest"),
                Text("in receiving the included information for "),
                Text('research and educational purposes.'),
                Text("This app may contain memes that are hateful/offensive"),
                Text(' to some individuals if you understand'),
                Text(
                    "the aforementioned statements   and agree to use the app write your id"),
                Text(
                    "and click enter, otherwise please uninstall this app or close it. "),
                Text(
                  '${get_errors()}',
                  style: Theme.of(context).textTheme.display1,
                ),
              ]),
            ),
          ),
          Container(

              padding: EdgeInsets.all(55),
              child: Column(
                  children : [
                  TextField(
                      obscureText: false,
                      decoration: InputDecoration(

                        labelText: 'Volunteer ID',
                      ),
                      onSubmitted: add_context),
                  ElevatedButton(onPressed: get_urls, child: Text('I agree')),
          ]
              )),
        ])));
  }
}
