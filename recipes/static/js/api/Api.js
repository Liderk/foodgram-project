class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
    }
    getToken () {
    if (document.getElementsByName('csrfmiddlewaretoken').length > 0) {
      return document.getElementsByName('csrfmiddlewaretoken')[0].value
    } else {
      return ''
    }
  }
  getPurchases () {
    return fetch(`/api/v1/purchases`, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addPurchases (id) {
    return fetch(`/api/v1/purchases/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      },
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removePurchases (id){
    return fetch(`/api/v1/purchases/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(`/api/v1/subscriptions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      },
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(`/api/v1/subscriptions/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(`/api/v1/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      },
      body: JSON.stringify({
        id: id
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(`/api/v1/favorites/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getToken()
      }
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(`/api/v1/ingredients/?search=${text}`, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getToken()
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
