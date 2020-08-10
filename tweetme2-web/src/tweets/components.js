import React, {useEffect, useState}  from 'react'

import {apiTweetCreate, apiTweetList, apiTweetAction} from './lookup'

export function TweetsComponent(props) {
    const textAreaRef = React.createRef()
    const [newTweets, setNewTweets] = useState([])
    const handleBackendUpdate = (response, status) => {
      let tempNewTweets = [...newTweets]
      console.log(response, status)
      if (status === 201){
        tempNewTweets.unshift(response)
        setNewTweets(tempNewTweets)
      } else {
        console.log(response)
        alert("An error occured please try again")
      }
    }
    const handleSubmit = (event) => {
      event.preventDefault()
      const newVal = textAreaRef.current.value
      // change this to a server side call
      apiTweetCreate(newVal, handleBackendUpdate) 
      textAreaRef.current.value = ''
    }
    return <div className={props.className}>
            <div className='col-12 mb-3'>
              <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'>

                </textarea>
                <button type='submit' className='btn btn-primary my-3'>Tweet</button>
            </form>
            </div>
        <TweetsList newTweets={newTweets} />
    </div>
}

export function TweetsList(props) {
    const [tweetsInit, setTweetsInit] = useState([])
    const [tweets, setTweets] = useState([])
    const [tweetsDidSet, setTweetsDidSet] = useState(false)
    useEffect(()=>{
      const final = [...props.newTweets].concat(tweetsInit)
      if (final.length !== tweets.length) {
        setTweets(final)
      }
    }, [props.newTweets, tweets, tweetsInit])

    useEffect(() => {
      if (tweetsDidSet === false){
        const handleTweetListLookup = (response, status) => {
          if (status === 200){
            setTweetsInit(response)
            setTweetsDidSet(true)
          } else {
            alert("There was an error")
          }
        }
        apiTweetList(handleTweetListLookup)
      }
    }, [tweetsInit, tweetsDidSet, setTweetsDidSet])
    const handleDidRetweet = (newtweet) => {
         const updateTweetsInit = [...tweetsInit]
         updateTweetsInit.unshift(newtweet)
         setTweetsInit(updateTweetsInit)
         const updateFinalTweets = [...tweets]
         updateFinalTweets.unshift(tweets)
         setTweets(updateFinalTweets)
    }
    return tweets.map((item, index)=>{
      return <Tweet tweet={item} didRetweet = {handleDidRetweet} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`} />
    })
  }


export function ActionBtn(props) {
    const {tweet, action, didPerformAction} = props
    const likes = tweet.likes ? tweet.likes : 0
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    
    const handleActionBackendEvent = (response, status) => {
      console.log(response, status)
      if ((status === 200 || status === 201) && (didPerformAction)){
        // setLikes(response.likes)
        didPerformAction(response, status)
      //  setUserLike(true)
      }
      // if (action.type === 'like') {
      //   if (userLike === true) {
      //     // perhaps i Unlike it?
      //     setLikes(likes - 1)
      //     setUserLike(false)
      //   } else {
      //     setLikes(likes + 1)
      //     setUserLike(true)
      //   }
        
      // }
    }
    
    const handleClick = (event) => {
      event.preventDefault()
      apiTweetAction(tweet.id, action.type, handleActionBackendEvent)
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
  }


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

  