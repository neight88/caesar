#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

page_header = '''
<html>
<head>

<title>Caesar</title>
</head>
<body>
'''

form = '''
    <form method="post">
        <div>
            <label for="rotate">Rotate by:</label>
            <input type="text" name="rotate" value="">
        </div>
        <div>
            <textarea type="text" name="text"></textarea>
            <input type="submit">
    </form>
'''

page_footer = '''
</body></html>
'''
def alphabet_position(letter):
    uncase = letter.upper()
    counter = 0
    for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if i == uncase:
            return counter
        counter += 1
    return counter

def rotate_character(char, rot):
    code1 = (alphabet_position(char) + int(rot)) % 26
    if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        newChar = chr((code1 + 65))
        return newChar
    elif char in "abcdefghijklmnopqrstuvwxyz":
        newChar = chr((code1 + 97))
        return newChar
    else:
        return char

def encrypt(text, rotation):
    codedStr = ""

    for i in text:
        codedChar = rotate_character(i, rotation)
        codedStr += codedChar
    return codedStr

class MainHandler(webapp2.RequestHandler):
    #def writeForm(self, rotate="", text=""):
    #    self.response.write(form)
    def get(self):
        self.response.write(page_header + form + page_footer)

    def post(self):
        rotate = cgi.escape(self.request.get("rotate"))
        uncoded = cgi.escape(self.request.get("text"))
        text = encrypt(uncoded, rotate)

        newform = '''
            <form method="post">
                <div>
                    <label for="rotate">Rotate by:</label>
                    <input type="text" name="rotate" value="{0}">
                </div>
                <div>
                    <textarea type="text" name="text">{1}</textarea>
                    <input type="submit">
            </form>
        '''.format(rotate,text)

        self.response.write(page_header + newform + page_footer)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
