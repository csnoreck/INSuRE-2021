The primary app is projectPrototype.py, wich runs a dash web app. To view the app, open a browser (tested with firefox) and go to 127.0.0.1:8050. 



To add/edit/remove scans to the program, follow these instructions.

1. Search for the string "CONFIGURE SCANS HERE" in projectPrototype.py.

2. There should only be three hits, the first declares the variables that hold the parsed file.

3. If you added or removed a file in the previous step (step 2), then the mergeDicts() function call needs to be updated accordingly.

4. If you added or removed a file in step 2, then the compileGraphData() function call under the third hit also needs to be updated acordingly. 