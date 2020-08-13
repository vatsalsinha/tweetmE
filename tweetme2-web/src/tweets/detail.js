import React, {useState}  from 'react'
import {ActionBtn} from './buttons'



export function ParentTweet(props){
    const {tweet} = props
    return (
      tweet.parent ? <div className = 'row'>
        <div className = 'col-11 mx-auto p-3 border rounded'>
          <p className='mb-0 text-muted small'>Retweet</p> 
          <Tweet hideActions className={' '} tweet= {tweet.parent} /> 
        </div>
      </div> : null
    )
  }
    
  export function Tweet(props) {
      const tweet = props.tweet // same as const {tweet} = props.tweet
      const didRetweet = props.didRetweet
      const hideActions = props.hideActions
      const [actionTweet, setActionTweet] = useState(props.tweet ? props.tweet : null)
      const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
      const handlePerformAction = (newActionTweet, status) => {
        if (status === 200){
          setActionTweet(newActionTweet)
        }else if(status === 201){
          //let the tweet list know
          if (didRetweet){
            didRetweet(newActionTweet)
          }
        }
      }
      return( 
        <div className={className}>
            <p>
              {tweet.id} - {tweet.content}
            </p>
            <div>
            <ParentTweet tweet = {tweet} />
          </div>
          {(actionTweet && hideActions !== true) && <div className='btn btn-group'>
            <ActionBtn tweet={actionTweet} didPerformAction = {handlePerformAction} action={{type: "like", display:"Likes"}}/>
            <ActionBtn tweet={actionTweet} didPerformAction = {handlePerformAction} action={{type: "unlike", display:"Unlike"}}/>
            <ActionBtn tweet={actionTweet} didPerformAction = {handlePerformAction} action={{type: "retweet", display:"Retweet"}}/>
          </div>}
      </div>
    )
  }
  
    