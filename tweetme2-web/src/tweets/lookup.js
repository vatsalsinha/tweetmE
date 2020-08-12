import {backendLookup} from '../lookup'

export function apiTweetCreate(newTweet, callback){
    backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
}

export function apiTweetDetail(tweetId, callback) {
    let endpoint = "/tweets/"
    if (tweetId){
        endpoint = `/tweets/${tweetId}`
    }
    backendLookup("GET", endpoint, callback)
}
  
export function apiTweetList(username, callback) {
    let endpoint = "/tweets/"
    if (username){
        endpoint = `/tweets/?username=${username}`
    }
    backendLookup("GET", endpoint, callback)
}

export function apiTweetAction(tweetId, action,  callback){
    const data = {id: tweetId, action: action}
    backendLookup("POST", "/tweets/action", callback, data)
}

