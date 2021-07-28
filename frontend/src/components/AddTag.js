import React,{useState} from 'react'

function AddTag(props)
{
    const[tag, setTag]=useState()
    
    function addTag(e){
        e.preventDefault()
        var body={}
        body["newtag"]=tag
        console.log(tag)
        fetch(
            process.env.REACT_APP_API_SERVER+"/notes/newtag",
            {
                method: 'POST',
                headers: { 'Accept' : 'application/json',
                'Content-type': 'application/json', 
            },
            body:JSON.stringify(body),
        }
        ).then(() => props.success("tag"))
        .catch(err => console.log(err))
    }

    return(

        <div>

            <form onSubmit={addTag}>

                <label className="form-label" htmlFor="newtag"> New Tag : </label>
                <input className="form-control-sm" type="text" placeholder="Enter Tag Name Here"
                name="newtag"
                onChange={(e) => setTag(e.target.value)}
                />

                <div className="Addbtn">
                <button className="btn btn-success btn-sm"
                type="submit"
                >Add</button>
                </div>
                
            </form>

        </div>
    )

}

export default AddTag