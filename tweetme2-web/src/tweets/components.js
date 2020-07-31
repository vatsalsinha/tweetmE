import React, {useState, useEffect} from 'react';
import {loadTweets} from '../lookup';


export function ActionBtn(props) {
    const {tweet, action} = props
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    const display = action.type === 'like' ? `${tweet.likes} ${actionDisplay}` : action.display
    const handleClick = (event) => {
      event.preventDefault()
      if (action.type === 'like'){
        console.log(tweet.likes + 1)
      }
    }
    return <button class={className} onClick = {handleClick}>{display}</button>
}
  
  
export function Tweet(props){
    const {tweet} = props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return (
        <div className={className}>
          <p>{tweet.id}-{tweet.content}</p>
          <div className = 'btn btn-group'>
            <ActionBtn tweet = {tweet} action = {{type: "like", display: "Likes"}} />
            <ActionBtn tweet = {tweet} action = {{type: "unlike", display: "unLike"}} />
            <ActionBtn tweet = {tweet} action = {{type: "retweet", display: "ReTweet"}} />
          </div>
        </div>
    )
}



export function TweetList(props){
  const [tweets, setTweets] = useState([])

  useEffect(() => {
    const myCallback = (response, status) => {
      if (status === 200){
        setTweets(response)
      } else {
        alert("There was an error")
      }
    }
    loadTweets(myCallback)
  }, [])

  return (
    tweets.map((item, index)=>{
      return <Tweet tweet = {item} key = {`${index}-{item.id}`} className = 'my-5 py-5 border bg-white text-dark'/>
    })
  )
}
