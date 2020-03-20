

function stringMode(txt) {
    return "<span class='s2'>" + txt + "</span>";
}
function keywordMode(txt) {
    return "<span class='k'>" + txt + "</span>";
}
function operatorMode(txt) {
    return "<span class='o'>" + txt + "</span>";
}
function numberMode(txt) {
    return "<span class='nb'>" + txt + "</span>";
}
function propertyMode(txt) {
    return "<span class='p'>" + txt + "</span>";
}
function commentMode(txt) {
    return "<span class='c'>" + txt + "</span>";
}
function skipMode(txt) {
    return txt
}
function declareMode(txt) {
    return "<span class='f'>" + txt + "</span>";
}

function getMinPos() {
    var i, arr = [];
    for (i = 0; i < arguments.length; i++) {
        if (arguments[i][0] > -1) {
        if (arr.length == 0 || arguments[i][0] < arr[0]) {arr = arguments[i];}
        }
    }
    if (arr.length == 0) {arr = arguments[i];}
    return arr;
}
function getKeywordPos(txt, func) {
    var words, i, pos, rpos = -1, rpos2 = -1, patt;
    words = ["and","elif","is","global","as","in","if","from","raise","for","except","finally","print","import","pass","return",
                "exec","else","break","not","with","assert","yield","try","while","continue","del","or","lambda","async","await",
                "True","False","def","class"];

    for (i = 0; i < words.length; i++) {
        pos = txt.indexOf(words[i]);
        if (pos > -1) {
        patt = /\W/g;
        if (txt.substr(pos + words[i].length,1).match(patt) && txt.substr(pos - 1,1).match(patt)) {
            if (pos > -1 && (rpos == -1 || pos < rpos)) {
            rpos = pos;
            rpos2 = rpos + words[i].length;
            }
        }
        } 
    }
    return [rpos, rpos2, func];
}
function getOperatorPos(txt, func) {
    var words, i, pos, rpos = -1, rpos2 = -1, patt;
    words = ["+", "-", '*', "/", "%", "^", "&", "|", "<=", "<<", ">", "~"];

    for (i = 0; i < words.length; i++) {
        pos = txt.indexOf(words[i]);
        if (pos > -1) {
        patt = /\W/g;
        if (txt.substr(pos + words[i].length,1).match(patt) && txt.substr(pos - 1,1).match(patt)) {
            if (pos > -1 && (rpos == -1 || pos < rpos)) {
            rpos = pos;
            rpos2 = rpos + words[i].length;
            }
        }
        } 
    }
    return [rpos, rpos2, func];
}
function getPos(txt, start, end, func) {
    var s, e;
    s = txt.search(start);
    e = txt.indexOf(end, s + (end.length));
    if (e == -1) {e = txt.length;}
    return [s, e + (end.length), func];
    }
function getNumPos(txt, func) {
    var arr = ["<br>", " ", ";", "(", "+", ")", "[", "]", ",", "&", ":", "{", "}", "/" ,"-", "*", "|", "%", "="], i, j, c, startpos = 0, endpos, word;
    console.log(txt)
    for (i = 0; i < txt.length; i++) {
        for (j = 0; j < arr.length; j++) {
        c = txt.substr(i, arr[j].length);
        if (c == arr[j]) {
            if (c == "-" && (txt.substr(i - 1, 1) == "e" || txt.substr(i - 1, 1) == "E")) {
            continue;
            }
            endpos = i;
            if (startpos < endpos) {
            word = txt.substring(startpos, endpos);
            if (!isNaN(word)) {return [startpos, endpos, func];}
            }
            i += arr[j].length;
            startpos = i;
            i -= 1;
            break;
        }
        }
    }  
    return [-1, -1, func];
}
function getPos(txt, start, end, func) {
    var s, e;
    s = txt.search(start);
    e = txt.indexOf(end, s + (end.length));
    if (e == -1) {e = txt.length;}
    return [s, e + (end.length), func];
    }

function pythonMode(txt) {
    var rest = txt, done = "", esc = [], i, cc, tt = "", sfnuttpos, dfnuttpos, compos, comlinepos, keywordpos, numpos, mypos, tagpos;

    while (true) {
        sfnuttpos = getPos(rest, "'", "'", stringMode);
        dfnuttpos = getPos(rest, '"', '"', stringMode);
        compos = getPos(rest, "'''", "'''", commentMode);
        comlinepos = getPos(rest, '#', "\n", commentMode);      
        numpos = getNumPos(rest, numberMode);
        keywordpos = getKeywordPos(rest, keywordMode);
        //operatorpos = getOperatorPos(rest, operatorMode);
        //defPos = getPos(rest, "def", "(", declareMode);
        tagpos = getPos(rest, "<", ">", skipMode);
        if (Math.max(numpos[0], sfnuttpos[0], dfnuttpos[0], compos[0], comlinepos[0], keywordpos[0], tagpos[0]) == -1) {break;}
        mypos = getMinPos(numpos, sfnuttpos, dfnuttpos, compos, comlinepos, keywordpos, tagpos);
        if (mypos[0] == -1) {break;}
        if (mypos[0] > -1) {
        done += rest.substring(0, mypos[0]);
        done += mypos[2](rest.substring(mypos[0], mypos[1]));
        rest = rest.substr(mypos[1]);
        }
    }
    rest = done + rest;
    return rest;
}

function pythonDecorate(element) {
    var elementText = element.innerHTML;
    
    elementText = pythonMode(elementText);
    
    element.innerHTML = elementText;
}
function syntaxHighlight(pythonElements) {
    for (var i = 0; i < pythonElements.length; i++) {
        pythonDecorate(pythonElements[i]);
    }
}

syntaxHighlight(document.getElementsByClassName("code"))
