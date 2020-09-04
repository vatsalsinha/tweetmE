import React, {useState, useEffect}  from 'react'
import {TweetsList} from './list'
import {apiTweetDetail} from './lookup'
import {TweetCreate} from './create'
import {Tweet} from './detail'
import {FeedList} from './feed'

export function FeedComponent(props) {
  const [newTweets, setNewTweets] = useState([])
  const canTweet = props.canTweet === "false" ? false : true
  const handleNewTweet = (newTweet) =>{
    let tempNewTweets = [...newTweets]
    tempNewTweets.unshift(newTweet)
    setNewTweets(tempNewTweets)
  }
  return <div className={props.className}>
          {canTweet === true && <TweetCreate didTweet={handleNewTweet} className='col-12 mb-3' />}
        <FeedList newTweets={newTweets} {...props} />
  </div>
}

export function TweetsComponent(props) {
  const canTweet = props.canTweet === "false" ? false:true
  const {username} = props
    const [newTweets, setNewTweets] = useState([])
    const handleNewTweet = (response, status) => {
      let tempNewTweets = [...newTweets]
      tempNewTweets.unshift(response)
      setNewTweets(tempNewTweets)
    }
    return <div className={props.className}>
            {canTweet === true && <TweetCreate didTweet = {handleNewTweet} className='col-12 mb-3' />}
        <TweetsList newTweets={newTweets} {...props}/>
    </div>
}

export function TweetDetailComponent(props){
  const tweetId = props.tweetId
  const [tweet, setTweet] = useState(null)
  const [didLookup, setDidLookup] = useState(false)
  const handleBackendLookup = (response, status) => {
    if (status === 200){
      setTweet(response)
    } else {
      alert("There was an error while fetching the tweet")
    }
  }
  useEffect(() => {
    if (didLookup === false){
      apiTweetDetail(tweetId, handleBackendLookup)
      setDidLookup(true)
    }
  }, [tweetId, didLookup, setDidLookup])
  return tweet === null ? null : <Tweet tweet= {tweet} className = {props.className}/>
}

