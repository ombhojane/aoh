# app.py

from flask import Flask, render_template, request, flash, redirect, url_for
import os
import google.generativeai as genai


app = Flask(__name__)


api = os.environ.get("GENAI_API_KEY")
genai.configure(api_key=api)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/planning', methods=['GET', 'POST'])
def planning():
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)

    if request.method == 'POST':
        product_description = request.form['product_description']
        prompt_parts = [
            f"""Generate a simple Mermaid diagram code for a {product_description}.
            The response should only include the raw Mermaid diagram code without any markdown or encapsulation syntax like triple backticks or the word 'mermaid' in a code block identifier. ie. I dont want ```mermaid or ``` coming in response. Just the inside raw Mermaid code. eg. stateDiagram-v2 then rest code
            
            Examples of Mermaid diagram syntax include:

            Example 1 (stateDiagram):
            stateDiagram-v2
    [*] --> Still
    Still --> [*]
    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]

            Example 2 (Sequence Diagram):
            sequenceDiagram
            participant User
            participant App
            participant Server
            User->>App: Open App
            App->>Server: Request Bus Route
            Server-->>App: Return Bus Route
            App->>Server: Request Ticket
            Server-->>App: Return Ticket

            Example 3 (mindmap):
            mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectivness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid

        """
        ]

        response = model.generate_content(prompt_parts)
        mermaid_code = response.text if response.text else "Diagram generation failed."
        return render_template("planning.html", mermaid_code=mermaid_code)
    else:
        return render_template("planning.html")


@app.route('/progress')
def new_page():
    return render_template('progress.html')

@app.route('/project')
def explore_demo():
    return render_template('project.html')


@app.route('/diagram')
def diagram():
    return render_template('diagram.html')

@app.route('/completions')
def complwtions():
    return render_template('completions.html')

if __name__ == "__main__":
    app.run(debug=True)
