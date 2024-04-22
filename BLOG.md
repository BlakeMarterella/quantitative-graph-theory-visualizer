# Qunatitative Graph Theory Vizualizer

## Getting Started

This tools was created with the intent to help individuals vizualize fluctations in the stock market, the performance of stock holdings overtime, and understand the underlying graph theory driving these changes. With this set of tools, users will be able to view the correlation between stocks and sectors to increase awareness of diversification and experiment with different portfolio allocations. There are additional tools to support future projects in the field of quantitative graph theory by exporting data generated on the site to CSV files.

### Features

- Stock Market Data Exportation Tool

## Software Design and Architecure

I knew that I wanted to use python in some way for this project because of the vast amount of libraries available for data manipulation and graph theory. To that end, I decided to use Flask because of its simplicity. In the future, I would like to implement an API with proper documentation to make the process of integrating datasets into future projects easier. Some of the libraries I am using are:

- Pandas: manipulate the data
- Numpy: to perform calculations
- NetworkX: create the graphs
- Matplotlib: display the graphs.

I also knew that I wanted to use a web framework to create a user interface for the project. I went with VueJS since I had some slight experience in the past. Angular is usually my go-to but I figured it would be too heavy and require more time to set-up. For additional asthetics, I am using TailwindCSS to style the site quickly. With just a few modifications to the `tailwind.config.js` file, I was able to give the site a unique color pallete and implement other uniform style classes throughout the site.

With that, I have a basic understanding of the tools I will be using and how they will interact with each other. I will now begin to set-up the project.

### Repository

I elected to go with a Mono-Repository design for this project. Having both the frontend and backend directory in the same repository will make it easier to manage the project as a whole. At some point, I would like a repository for both the frontend and backend especially if I begin getting support from contributors. For the time being, I will be using the following directory structure:

```
quantitative-graph-theory-visualizer
├── frontend
│   ├── <my vue project>
│
├── backend
│   ├── <my flask project>
│
├── README.md
├── BLOG.md
├── LICENSE
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .env
├── .env.example
├── .git
├── .github
├── .vscode
├── .idea
|_
```

You can view the most up to date version of the project on the [GitHub Repository](https://github.com/BlakeMarterella/quantitative-graph-theory-visualizer)

### Set-Up Frontend

To create a new VueJS project with TailwindCSS, use the Vite to set up a new project. Instructions for how to do this can be found on [Tailwind CSS's official documentation](https://v2.tailwindcss.com/docs/guides/vue-3-vite). Alternatively, you can follow the instructions below:

```shell
# Create a new vite project
npm init vite frontend

# You are now in the directory of your new project!
cd frontend

# Install Vite's front-end dependencies
npm install
```

Next, you will need to install TailwindCSS and its dependencies. You can do this by running the following commands:

```shell
# Install Tailwind and its dependencies
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest

# Create configuration files
npx tailwindcss init -p
```

If you follow the guide above, you will learn more about further optimizations with TailwindCSS. For now, I will be using the default configuration. You can now start the development server with the following command:

```shell
# Start the development server
npm run dev
```

### Set-Up Backend

To create the Flask backend requires a little more manual labor than creating a new frontend project but it's simple with the steps below:

```shell
# Create a new directory for the backend
mkdir backend
cd backend

# Create a new virtual environment
python3 -m venv venv

# Activate the new virtual environment (you will need to do this anytime you close your terminal)
source venv/bin/activate

# Install Flask
pip install Flask
```

Now you will need to create the entry point to your flask app:

```shell
# Create a new file called app.py
touch app.py
```

My project all started with this sample code:

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```
