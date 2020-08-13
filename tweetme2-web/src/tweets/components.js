import React, {useState}  from 'react'
import {TweetsList} from './list'
import {apiTweetCreate} from './lookup'
import {TweetCreate} from './create'

export function TweetsComponent(props) {
  const canTweet = props.canTweet === "false" ? false:true
  const {username} = props
    console.log(props)
    const [newTweets, setNewTweets] = useState([])
    const handleNewTweet = (response, status) => {
      let tempNewTweets = [...newTweets]
      tempNewTweets.unshift(response)
      setNewTweets(tempNewTweets)
      console.log(response, status) 
    }
    return <div className={props.className}>
            {canTweet === true && <TweetCreate didTweet = {handleNewTweet} className='col-12 mb-3' />}
        <TweetsList newTweets={newTweets} {...props}/>
    </div>
}



