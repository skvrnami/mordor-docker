from flask import Flask, request, Response
import sys
from ufal.morphodita import *

def encode_entities(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

tagger_file = "czech-morfflex-pdt-161115.tagger"
sys.stderr.write('Loading tagger: ')
tagger = Tagger.load(tagger_file)
if not tagger:
    sys.stderr.write("Cannot load tagger from file '%s'\n" % sys.argv[1])
    sys.exit(1)
sys.stderr.write('done\n')

forms = Forms()
lemmas = TaggedLemmas()
tokens = TokenRanges()
tokenizer = tagger.newTokenizer()
if tokenizer is None:
    sys.stderr.write("No tokenizer is defined for the supplied model!")
    sys.exit(1)


app = Flask(__name__)

@app.route("/", methods=['GET'])
def tag():
    text = request.args.get('text')
    tokenizer.setText(text)
    t = 0
    out = ""

    while tokenizer.nextSentence(forms, tokens):
        tagger.tag(forms, lemmas)
        for i in range(len(lemmas)):
            lemma = lemmas[i]
            token = tokens[i]
            out = out + ('%s%s<token lemma="%s" tag="%s">%s</token>%s' % (
            encode_entities(text[t : token.start]),
            "<sentence>" if i == 0 else "",
            encode_entities(lemma.lemma),
            encode_entities(lemma.tag),
            encode_entities(text[token.start : token.start + token.length]),
            "</sentence>" if i + 1 == len(lemmas) else "",
            ))
            t = token.start + token.length
        #print(encode_entities(text[t : ]))

    #print(out)
    # html = "{tagged_output}"
    return Response(out, mimetype='text/xml')
    #return html.format(tagged_output=out)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
