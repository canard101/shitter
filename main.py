from flask import Flask, request, render_template
import random
from datetime import datetime
from tinydb import TinyDB, Query
from replit import db as debe

db = TinyDB("database.json")

app = Flask("Shitter")
users = TinyDB("users.json")
users_table = users.table("users")


@app.route("/", methods=["GET"])
def home():
    if request.remote_addr in open("ipdb").read():
        pass
    else:
        open("ipdb", "a").write(str(request.remote_addr) + "\n")
    return return_website()


def return_website():
    posts = list(reversed(TinyDB("database.json").all()))
    postscode = ""
    htmlcode = open("index.html").read()
    for post in range(0, len(posts)):

        post_content = posts[post]["content"]
        final_content = ""
        count = 0
        for char in post_content:
            final_content += char
            count += 1
            if count % 42 == 0:
                final_content += ""

        if len(final_content) >= 336:
            final_content = final_content[0:335] + "... <u>READ MORE</u>"
        else:
            pass

        #if len(posts[post]["content"]) >
        if posts[post]["isReply"] is True:
            Post = Query()
            result = db.search(Post.id == posts[post]["repliedID"])
            
            postscode += (
            '<a href="https://shitter.ch/post/'
            + posts[post]["id"]
            + '">'
            + '<p width="560px" style="font-size: 20px; border: 2px solid #BCB1AE; border-radius: 5px; margin-top: 70px; margin-right: 70px; margin-bottom: 10px; margin-left: 70px; padding: 30px; overflow: hidden;"><b>'
            + '<img src="'
            + posts[post]["profile_picture"]
            + '" class="pp"><br/>'
            + '<span style="color: #623700; text-decoration-color: #623700; text-decoration: underline;" id="lepseudoenelsuroestedeespana">'
            + posts[post]["pseudo"]
            + "</span></b>"
            + '<br /><br /></a>Replying to @<a style="color: blue; text-decoration-color: blue; text-decoration: underline;" target="_blank" href="https://shitter.ch/post/' 
            + result[0]["id"]
            + '">'
            + result[0]["pseudo"] 
            + "</a><br/><br/>" + '<a class="postlink" href="https://shitter.ch/post/'
            + posts[post]["id"]
            + '"> '
            + final_content
            + "<br /><br />❤️"
            + str(posts[post]["likes"])
            + "<br /><p style='font-size: 12; font-color: grey;'> <span id='postdate' style='font-size: 8'>"
            + posts[post]["date"]
            + "</span></a></p></p>"
            )    
        else:
            try:

                postscode += (
                '<a href="https://shitter.ch/post/' + posts[post]["id"] + '" >'
                + '<p width="560px" style="font-size: 20px; border: 2px solid #BCB1AE; border-radius: 5px; margin-top: 70px; margin-right: 70px; margin-bottom: 10px; margin-left: 70px; padding: 30px; overflow: hidden;"><b>'
                + '<img src="'
                + posts[post]["profile_picture"]
                + '" class="pp"><br/>'
                + '<span style="color: #623700; text-decoration-color: #623700; text-decoration: underline;" id="lepseudoenelsuroestedeespana">'
                + posts[post]["pseudo"]
                + "</span></b>"
                +"</i><br/><br/>"
                + final_content
                + "</a><br /><br />❤️"
                + str(posts[post]["likes"])
                + "<br /><p style='font-size: 12; font-color: grey;'> <span id='postdate' style='font-size: 8'>"
                + posts[post]["date"]
                + "</span></p></p>"
                )
            except KeyError:
                postscode += (
                '<a href="https://shitter.ch/post/' + posts[post]["id"] +
                '"> <li style="font-size: 20px; border: 2px solid #BCB1AE; border-radius: 5px; margin-top: 70px; margin-right: 70px; margin-bottom: 10px; margin-left: 70px; padding: 30px; overflow: hidden;"><b>'
                +
                '<span style="color: #623700; text-decoration-color: #623700; text-decoration: underline;">'
                + posts[post]["pseudo"] + '</span></b>' + "<br /><br />" +
                posts[post]["content"] + "<br /><br />❤️" +
                str(posts[post]["likes"]) +
                "<br /><p style='font-size: 12; font-color: grey;'> <span id='postdate' style='font-size: 8'>"
                + posts[post]["date"] + "</span></a></p></li>")
    htmlcode = htmlcode.replace("{{POSTS}}", postscode)
    return htmlcode


def redirect():
    return '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=\'https://shitter.ch/\'" /></head><body></body></html>'


def redirect_to_post(id):
    return (
        '<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=\'https://shitter.ch/post/'
        + id + "'\" /></head><body></body></html>")


@app.route("/404")
def error404():
    htmlcode = open("404.html").read()
    return htmlcode


@app.route("/gotosignup")
def gotosignup():
    htmlcode = open("signup.html").read()
    return htmlcode


@app.route("/gotomakepost")
def gotomakepost():
    htmlcode = open("makepost.html").read()
    return htmlcode


@app.route("/gotomainpage")
def gotomainpage():
    htmlcode = open("index.html").read()
    return htmlcode


@app.route("/about")
def about():
    htmlcode = open("about.html").read()
    return htmlcode


@app.route("/leaderboard")
def leaderboard():
    htmlcode = open("posts.html").read()
    users = debe.keys()
    leaderboarddb = {}
    for user in users:
        leaderboarddb[user] = debe[user]
    sorted_keys = sorted(leaderboarddb.keys(),
                         key=lambda x: leaderboarddb[x],
                         reverse=True)
    htmlcode += ("<h2><li><b><u>" + sorted_keys[0] +
                 "</u></b> is on the top of the podium with a total of " +
                 str(leaderboarddb[sorted_keys[0]]) + " posts !</li></h2>")
    for usr in range(1, len(sorted_keys)):
        htmlcode += ("<li><u>" + sorted_keys[usr] + "</u> : " +
                     str(leaderboarddb[sorted_keys[usr]]) + " posts </i>")
    htmlcode = htmlcode.replace(
        "{{CSS}}", "<style>" + open("style.css").read() + "</style>")
    htmlcode += "</body>"
    htmlcode += (
        "<html><footer><p>Created by Platypus Studio and Krayse</p></html></footer>"
    )
    return htmlcode


@app.route("/postsdb")
def ips():
    return open("database.json").read()


def stylize(text):

    text = text.replace(
        "<script>",
        "User tried to hack shitter.ch with this code : </b>\\n\\n")
    text = text.replace("<img>",
                        "User tried to hack shitter.ch with a weird image")
    text = text.replace("\\n", "<br />")
    text = text.replace("[b]", "<b>")
    text = text.replace("[/b]", "</b>")
    text = text.replace("[i]", "<i>")
    text = text.replace("[/i]", "</i>")
    text = text.replace("[u]", "<u>")
    text = text.replace("[/u]", "</u>")
    text = text.replace("[h1]", "<h1>")
    text = text.replace("[/h1]", "</h1>")
    text = text.replace("[h2]", "<h2>")
    text = text.replace("[/h2]", "</h2>")
    text = text.replace("[h3]", "<h3>")
    text = text.replace("[/h3]", "</h3>")
    text = text.replace("[h4]", "<h4>")
    text = text.replace("[/h4]", "</h4>")
    text = text.replace("[h5]", "<h5>")
    text = text.replace("[/h5]", "</h5>")
    text = text.replace("[h6]", "<h6>")
    text = text.replace("[/h6]", "</h6>")
    text = text.replace("[p]", "<p>")
    text = text.replace("[/p]", "</p>")
    text = text.replace("[br]", "<br/>")
    text = text.replace("[img]", '<img width="200px" src="')
    text = text.replace("[/img]", '"></img>')
    text = text.replace(
        "[yt]",
        '<iframe width="500" height="300" src="https://youtube.com/embed/')
    text = text.replace(
        "[/yt]",
        '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>',
    )
    text = text.replace("[a]", '<a href="')
    text = text.replace("[/a]", '"></a>')
    text = text.replace("[blue]", "<font color='blue'>")
    text = text.replace("[/blue]", "</font>")
    text = text.replace("[red]", "<font color='red'>")
    text = text.replace("[/red]", "</font>")
    text = text.replace("[yellow]", "<font color='yellow'>")
    text = text.replace("[/yellow]", "</font>")
    text = text.replace("[lime]", "<font color='lime'>")
    text = text.replace("[/lime]", "</font>")
    text = text.replace("[green]", "<font color='green'>")
    text = text.replace("[/green]", "</font>")
    return text


@app.route("/newpost/", methods=["POST"])
def add_post():
    canPost = False
    author = request.form["pseudo"]
    if author == "":
        author = "Anonymous"
    else:
        pass
    while True:
        id = random.randint(1, 99999999)
        if len(str(id)) == 1:
            id = "0000000" + str(id)
        if len(str(id)) == 2:
            id = "000000" + str(id)
        if len(str(id)) == 3:
            id = "00000" + str(id)
        if len(str(id)) == 4:
            id = "0000" + str(id)
        if len(str(id)) == 5:
            id = "000" + str(id)
        if len(str(id)) == 6:
            id = "00" + str(id)
        if len(str(id)) == 7:
            id = "00" + str(id)
        else:
            id = id
            pass
        if str(id) in open("database.json").read():
            pass
        else:
            break
    canPost = True
    blacklist = open("blacklist.txt").read()
    blacklist = blacklist.splitlines()
    for word in blacklist:
        if word in request.form["content"].lower():
            canPost = False
        else:
            pass
    if canPost:
        db.insert({
            "pseudo":
            author,
            "content":
            stylize(request.form["content"]),
            "date":
            datetime.today().strftime("%Y/%m/%d %H:%M"),
            "likes":
            0,
            "profile_picture":
            "https://api.dicebear.com/6.x/thumbs/png?seed=" + author, 
            "isReply": False,
            "id":
            str(id),
            "comments": [],
        })
    else:
        pass
    return redirect()


@app.route("/post/<id>")
def postdetail(id):
    print("test 1 passed")
    html_code = open("postdetail.html").read()
    Post = Query()
    result = db.search(Post.id == id)

    pseudo = result[0]["pseudo"]
    content = result[0]["content"]

    post_content = content
    final_content = ""
    count = 0
    for char in post_content:
        final_content += char
        count += 1
        if count % 68 == 0:
            final_content += ""
    
    html_code = html_code.replace("{postid}", id)
    html_code = html_code.replace("{author}", pseudo)
    html_code = html_code.replace("{content}", final_content)
    html_code = html_code.replace("{link}", id)
    html_code = html_code.replace("{likes}", str(result[0]["likes"]))
    html_code = html_code.replace(
        "{profile_picture}",
        '<img src="' + str(result[0]["profile_picture"]) + '" class="pp"')
    commentsvar = ""
    for i in range(0, len(result[0]["comments"]), 2):
        pseudo = result[0]["comments"][i]
        text = result[0]["comments"][i + 1]
        commentsvar += "<br /><h3>"+pseudo+" : "+text
    #print(html_code)
    html_code = html_code.replace("{COMMENTS}", commentsvar)
    return html_code




@app.route("/replypage/<id>")
def replypage(id):
    html_code = open("replypage.html").read()
    Post = Query()
    result = db.search(Post.id == id)

    html_code = html_code.replace("{USER}", result[0]["pseudo"])
    html_code = html_code.replace("{id}", id)
    return html_code


@app.route("/like/<id>")
def like(id):
    Post = Query()
    result = db.search(Post.id == id)
    likes = result[0]["likes"]
    nouveau_nombre_likes = likes + 1
    db.update({"likes": nouveau_nombre_likes}, Post.id == id)
    """html_code = post_detail(id)
    return html_code"""
    return redirect_to_post(id)

@app.route("/comment/<commentedID>", methods=["POST"])
def comment(commentedID):
    print("test 69 passed")
    commentedObject = Query()
    result = db.search(commentedObject.id == commentedID)
    db.update({"comments": result[0]["comments"] + [request.form["pseudo"], request.form["content"]]})

    return redirect_to_post(commentedID)

    

@app.route("/reply/<repliedid>", methods=["POST"])
def reply(repliedid):
    canPost = False
    author = request.form["pseudo"]
    if author == "":
        author = "Anonymous"
    else:
        pass
    while True:
        id = random.randint(1, 99999999)
        if len(str(id)) == 1:
            id = "0000000" + str(id)
        if len(str(id)) == 2:
            id = "000000" + str(id)
        if len(str(id)) == 3:
            id = "00000" + str(id)
        if len(str(id)) == 4:
            id = "0000" + str(id)
        if len(str(id)) == 5:
            id = "000" + str(id)
        if len(str(id)) == 6:
            id = "00" + str(id)
        if len(str(id)) == 7:
            id = "00" + str(id)
        else:
            id = id
            pass
        if str(id) in open("database.json").read():
            pass
        else:
            break
    canPost = True
    blacklist = open("blacklist.txt").read()
    blacklist = blacklist.splitlines()
    for word in blacklist:
        if word in request.form["content"].lower():
            canPost = False
        else:
            pass
    if canPost:
        repliedobject = Query()
        result = db.search(repliedobject.id == repliedid)
        usertoreply = result[0]["pseudo"]
        
        db.insert({
            "pseudo":
            author,
            "content":
            stylize(request.form["content"]),
            "date":
            datetime.today().strftime("%Y/%m/%d %H:%M"),
            "likes":
            0,
            "profile_picture":
            "https://api.dicebear.com/6.x/thumbs/png?seed=" + author,
            "isReply": True,
            "repliedID": result[0]["id"],
            "id":
            str(id),
        })
    else:
        pass
    return redirect()

@app.route("/user/<pseudo>", methods=["GET"])
def userpage(pseudo):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0")
