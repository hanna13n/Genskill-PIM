import React, {useState} from 'react'


function EditNote(props){

    var tags={}
    
    const id=props.note.note.id
    const[title, setTitle]=useState(props.note.note.title)
    const[detail, setDetail]=useState(props.note.note.detail)
    // const[tags, setTags]=useState(props.tags.tags)

    props.tags.tags.forEach(element => {
        if(!props.note.note.tags.includes(element[0]))
            tags[element[0]]=false
        else
            tags[element[0]]=true
    });


    function updateNote(e) {
         e.preventDefault();
         tags["title"]=title
         tags["detail"]=detail
         
         fetch(
            process.env.REACT_APP_API_SERVER+"/notes/"+id+"/edit", 
            {
                method: 'POST',
                headers: { 'Accept' : 'application/json',
                'Content-type': 'application/json',
             },
             body:JSON.stringify(tags),
            }
         ).then(resp => {props.success("note",id)})
    }

    return(
        <div>
            {props.note &&
            <form  onSubmit={updateNote} >

                <label htmlFor="title" className="form-label">Title : </label>
                <input type="text" className="form-control-sm" 
                placeholder="Enter Title" 
                value={title}
                name="title"
                onChange={(e) => setTitle(e.target.value)}
                />
                <br/>

                <textarea className="form-control-sm" name="detail" id="detail" cols="50" rows="5" 
                value={detail} 
                placeholder="...note..."
                onChange={(e) => setDetail(e.target.value)} />

                <div className="tagcheckbox">
                {props.tags.tags &&
                    props.tags.tags.map(tag =>
                    {
                        return(
                            <span key={tag} className="checkbox">
                            {tags[tag[0]] ? 
                            <span>
                            <input className="form-check-input" type="checkbox" name={tag} id={tag} defaultChecked onChange={(e) => tags[e.target.name]=e.target.checked} />
                            <label className="form-check-label" htmlFor={tag}>{tag}</label> 
                            </span>
                            :
                            <span>
                            <input className="form-check-input" type="checkbox" name={tag} id={tag} onChange={(e) =>
                            tags[e.target.name]=e.target.checked} />
                            <label className="form-check-label" htmlFor={tag}>{tag}</label>
                            </span>
                            }

                            </span>
                        )
                    })
                }
                </div>
                <div className="Addbtn">
                <button className="btn btn-success"
                type="submit"
                >Save</button>
                </div>
            </form>
            }
        </div>
    )
}

export default EditNote