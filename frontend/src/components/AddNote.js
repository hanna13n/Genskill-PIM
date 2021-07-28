import React,{useState} from 'react'

function AddNote(props){

    var tags={}
    const[title, setTitle]=useState()
    const[detail, setDetail]=useState()

    props.tags.tags.forEach(element => {
            tags[element[0]]=false
    });

    function addNote(e){
        e.preventDefault()
        tags["title"]=title
        tags["detail"]=detail
    
        fetch(
            process.env.REACT_APP_API_SERVER+"/notes/addnew", 
            {
                method: 'POST',
                headers: { 'Accept' : 'application/json',
                'Content-type': 'application/json',
             },
             body:JSON.stringify(tags),
            }
         ).then(()=> props.success("note"))
         .catch(err => console.log(err))
    }


    return(
        <div>
            <form onSubmit={addNote}>

                <label htmlFor="title" className="form-label">Title : </label>
                <input className="form-control-sm" type='text' placeholder="Enter Title Here"
                    name="title"
                    onChange={(e) => setTitle(e.target.value)}
                />
                <br/>

                <textarea name="detail"
                cols="50" rows="5" className="form-control-sm"
                placeholder="Add Notes Here"
                onChange={(e) => setDetail(e.target.value)}
                />

                <div className="tagcheckbox"> 
                {props.tags.tags &&
                    props.tags.tags.map(tag =>
                    {
                        
                        return(
                            <span key={tag} className="checkbox">
                            <input type="checkbox" className="form-check-input"
                            name={tag}
                            onChange={(e) =>
                            tags[e.target.name]=e.target.checked}/>
                            <label className="form-check-label" htmlFor={tag}>{tag}</label>
                            </span>
                        )
                    })
                }
                </div>
                <div className="Addbtn">
                <button className="btn btn-success btn-sm"
                type="submit"
                >Add</button>
                </div>
            </form>
        </div>
    )
}

export default AddNote