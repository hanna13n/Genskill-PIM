import datetime
from flask import Blueprint
from flask import render_template, request, redirect, url_for, g, jsonify
from . import db

bp = Blueprint("notes", "notes", url_prefix="/notes")


@bp.route("/addnew", methods=["GET","POST"])
def addnote():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select tagname from hashtags")
    tags=(x[0] for x in cursor.fetchall())
    mark={}
    if request.method=="GET":
        return render_template("notes/addnote.html", tags=tags)

    elif request.method=="POST":
        title = request.form.get("title")
        detail = request.form.get("detail")
        for t in tags:
            mark[t]=request.form.get(f"{t}")
        created_on = datetime.datetime.now()
    
        cursor.execute("insert into notes (title,created_on, detail)values (%s, %s, %s)", (title, created_on,detail,))
        
        cursor.execute("select tagname from hashtags")
        tags=(x[0] for x in cursor.fetchall())
        
        for t in tags:
            if mark[t]:
                cursor.execute("""insert into tags_notes (note, tag) values ((select id from notes where detail=%s),
                (select id from hashtags where tagname=%s))""",(detail,t,))
        conn.commit()
        return redirect(url_for('index'),302)


@bp.route("/")
def allnotes():
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(
        "select id, title, created_on from notes order by created_on desc"
    )
    notes = cursor.fetchall()

    if(request.accept_mimetypes.best == "application/json"):
        return jsonify(dict(notes=[dict(id=id, title=title) for id, _, title, _, _ in notes]))
    else:
        return render_template("notes/noteslist.html", notes=notes)


@bp.route("/<nid>")
def notedetail(nid):
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute(
        "select title, created_on, detail from notes where id=%s", (nid,)
    )
    note = cursor.fetchone()
    cursor.execute(
        "select t.tagname from hashtags t, tags_notes tn where t.id=tn.tag and tn.note=%s",(nid,)
        )
    tags=(x[0] for x in cursor.fetchall())
    tags=list(tags)
    if not note:
        if(request.accept_mimetypes.best == "application/json"):
            return jsonify({"error": f"No note with id {nid}"})
        else:
            return render_template("notes/notedetail.html"), 404

    title, created_on, detail = note
    nid = int(nid)
    if nid == 1:
        prev = None
    else:
        prev = nid-1
    nxt = nid+1

    if(request.accept_mimetypes.best == "application/json"):
        ret = dict(
            id=nid,
            detail=detail,
            title=title,
            created_on=created_on,
            tags=tags
        )
        return jsonify(ret)
    else: 
        return render_template("notes/notedetail.html", nid=nid, detail=detail, prev=prev, nxt=nxt, title=title, created_on=created_on, tags=tags)


@bp.route("/<nid>/edit", methods=["GET", "POST", ])
def editnote(nid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(
        "select title, created_on, detail from notes where id=%s", (nid,)
    )
    note = cursor.fetchone()
    cursor.execute(
        "select t.tagname from hashtags t, tags_notes tn where t.id=tn.tag and tn.note=%s",(nid,)
        )
    tags=(x[0] for x in cursor.fetchall())
    tags=list(tags)
    cursor.execute(
        "select tagname from hashtags"
    )
    
    alltags=(x[0] for x in cursor.fetchall())
    alltags=list(alltags)

    if not note:
        if(request.accept_mimetypes.best == "application/json"):
            return jsonify({"error": f"No note with id {nid}"})
        else:
            return render_template("notes/notedetail.html"), 404

    if request.method=="GET":
        title, created_on, detail = note
        return render_template("notes/editnote.html",
        nid=nid,
        detail=detail,
        created_on=created_on,
        title=title,
        tags=tags,
        alltags=alltags)
    
    elif request.method=="POST":
        title=request.form.get("title")
        detail=request.form.get("detail")
    
        for t in alltags:
            if request.form.get(f"{t}"):
                if t not in tags:
                    cursor.execute(
                        "insert into tags_notes(note,tag)values (%s,(select id from hashtags where tagname=%s))",(nid,t,)
                    )
            else:
                if t in tags:
                    cursor.execute(
                        "delete from tags_notes where note=%s and tag=(select id from hashtags where tagname=%s)",(nid,t,)
                    )
        cursor.execute(
            "update notes set title=%s, detail=%s where id=%s",(title,detail,nid)
        )
        conn.commit()
        return redirect(url_for("notes.notedetail",nid=nid),302)

@bp.route("/deletenote/<nid>")
def deletenote(nid):
    conn=db.get_db()
    cursor=conn.cursor()
    cursor.execute(
        "delete from tags_notes where note=%s", (nid,)
    )
    cursor.execute(
        "delete from notes where id=%s",(nid,)
    )
    conn.commit()
    return redirect(url_for("notes.allnotes"),302)  
    


@bp.route("/newtag",methods=["GET","POST"])
def newtag():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method=="GET":
        return render_template("notes/newtag.html")
    elif request.method=="POST":
        newtag=request.form.get("newtag")
        cursor.execute("insert into hashtags (tagname) values (%s)",(newtag,))
        conn.commit()
        return redirect(url_for('index'),302)