import React from 'react'

import {apiTweetAction} from './lookup'

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
