import React from 'react'

export function UserLink(props){
    const {username} = props
    const handleUserLink = (event) => {
      window.location.href = `/profile/${username}`
    }
    return (
      <span className = 'pointer' onClick = {handleUserLink}>
        {props.children}
      </span>
    )
  }
  
export function UserDisplay(props){
    const {user, includeFullName, hideLink} = props
    const nameDisplay = includeFullName === true ? `${user.first_name} ${user.last_name}` : null;
    return (
      <React.Fragment>
        {nameDisplay}{' '}
        {hideLink === true ? `@${user.username}` : <UserLink username = {user.username} >
          @{user.username}{' '} 
          <span className = 'small text-muted'>
            <br/>
            {user.followers_count} followers {" "} {user.following_count} following
            <br/>
            <span className="glyphicon glyphicon-map-marker" aria-hidden="true">{user.location}</span>
            <br />
          </span>
        </UserLink>}
      </React.Fragment>
    )
  }
  
export function UserPicture(props){
    const {user, hideLink} = props
    const userIdSpan =  <span className='mx-1 px-3 py-2 rounded-circle bg-dark text-white'>
    {user.username[0]}
  </span>
    return  hideLink === true ? userIdSpan : <UserLink username = {user.username} > {userIdSpan}</UserLink>
  }