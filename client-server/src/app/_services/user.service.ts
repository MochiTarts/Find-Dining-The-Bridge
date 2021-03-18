import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

//const API_URL = 'http://localhost:8080/api/test/';
const API_URL = '/api/';
//const API_URL = '/';
const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) { }

  private static readonly AUTH_ENDPOINT = '/user';
  private static readonly UPLOAD_ENDPOINT = '/cloud_storage/upload/';
  private static readonly FAV_ENDPOINT = '/restaurant';



  // a get request to Django that has a template containing csrf token will set the token in the cookie
  // this is needed for Django to handle api calls from the browser
  setCSRFToken(): Observable<any> {
    return this.http.get(API_URL + 'admin', { responseType: 'text' });
  }

  // below are just testing for getting contents from the backend
  getPublicContent(): Observable<any> {
    return this.http.get(API_URL + 'all', { responseType: 'text' });
  }

  getUserBoard(): Observable<any> {
    return this.http.get(API_URL + 'user', { responseType: 'text' });
  }

  getROBoard(): Observable<any> {
    return this.http.get(API_URL + 'ro', { responseType: 'text' });
  }

  /*
  @Input: JSON object from auth
  @Output: Return all fields of a user
  Get all fields of a user
  */
  getConsumer(userData): Observable<any> {
    const endpoint = API_URL + 'consumer_subscriber_data/';
    const userObject = {
      email: userData.email,
      idToken: userData.idToken
    };
    return this.http.get(endpoint, { params: userObject });
  }

  /*
  @Input: JSON object from auth
  @Output: Return all fields of a user
  Get all fields of a user
  */
  getOwner(userData): Observable<any> {
    const endpoint = API_URL + 'restaurant_owner_data/';
    const userObject = {
      email: userData.email,
      idToken: userData.idToken
    };
    return this.http.get(endpoint, { params: userObject });
  }


  editConsumer(userData): Observable<any> {
    const endpoint = API_URL + 'consumer_subscriber_edit/';
    const userToken = {
      idToken: userData.idToken,
    };
    delete userData.idToken;
    return this.http.post<any>(endpoint, userData, { params: userToken });
  }


  editOwner(userData): Observable<any> {
    const endpoint = API_URL + 'restaurant_owner_edit/';
    const userToken = {
      idToken: userData.idToken,
    };
    delete userData.idToken;
    return this.http.post<any>(endpoint, userData, { params: userToken });
  }

  getNearbyRestaurantsConsumer(userData): Observable<any> {
    const endpoint = API_URL + 'consumer_subscriber_get_nearby/';
    const userObject = {
      email: userData.email
    };
    return this.http.get(endpoint, { params: userObject });
  }

  getNearbyRestaurantsOwner(userData): Observable<any> {
    const endpoint = API_URL + 'restaurant_owner_get_nearby/';
    const userObject = {
      email: userData.email
    };
    return this.http.get(endpoint, { params: userObject });
  }

  /*
  @Input: JSON user-restaurant favourite object
  @Output: Message from request or error
  Add a new restaurant to a user's list of favourites
  */
  addFavouriteRestaurant(data): Observable<any> {
    const endpoint = API_URL + 'user/add_favourite/'
    return this.http.post<any>(endpoint, data)
  }

  /*
  @Input: email of user whose list of favourites will be retrieved
  @Output: List of favourited restaurants
  Get all restaurants favourited by a user
  */
  getFavouriteRestaurants(email): Observable<any> {
    const endpoint = API_URL + 'user/get_favourites/'
    const paramObject = {
      'user': email
    }
    return this.http.get(endpoint, { params: paramObject })
  }

  /*
  @Input: JSON user-restaurant favourite object
  @Output: Message from request
  Removes a restaurant from a user's list of favourites
  */
  removeFavRestaurant(data): Observable<any> {
    const endpoint = API_URL + 'user/remove_favourite/'
    return this.http.post<any>(endpoint, data)
  }


  /*
  @Input: JSON object from auth
  @Output: Return True if user is in database, False otherwise
  Check if user exists in the database
  */
  editUser(userData): Observable<any> {
    const endpoint = API_URL + 'edit/';
    const userToken = {
      idToken: userData.idToken,
    };
    delete userData.idToken;
    return this.http.post<any>(endpoint, userData, { params: userToken });
  }

  /*
  @Input: JSON object from auth
  @Output: Return True if user is in database, False otherwise
  Check if user exists in the database
  */
  checkUserExists(userData): Observable<any> {
    const endpoint = API_URL + 'exists/';
    const userObject = {
      email: userData.email,
    };
    return this.http.get(endpoint, { params: userObject });
  }

  uploadUserMedia(formData, id): Observable<any> {
    const endpoint = API_URL + UserService.UPLOAD_ENDPOINT;

    formData.append('save_location', 'picture');
    formData.append('app', 'user_SDUserMedia');
    formData.append('email', id);

    return this.http.post<any>(endpoint, formData);
  }

  /*
  @Input: JSON object from auth
  @Output: None
  Update user in the database after logging in
  */
  updateUserInfo(userData): Observable<any> {
    const endpoint = API_URL + 'user/update/';
    return this.http.post<any>(endpoint, userData);
  }

  /*
  @Input: JSON object from auth
  @Output: None
  Edit consumer's consent status
  */
  editConsentStatus(userData): void {
    const endpoint = API_URL + 'user/consent_status/';
    const userToken = {
      idToken: userData.idToken,
    };
    delete userData.idToken;
    this.http.post<any>(endpoint, userData, { params: userToken }).subscribe((data) => { });
  }

  /*
  @Input: None
  @Output: None
  Deactivate user account
  */
  deactivateUser(id:string): Observable<any> {
    const endpoint = API_URL + 'user/deactivate/';
    return this.http.post<any>(endpoint, JSON.stringify({'id':id}), httpOptions);
  }

  getNearbyRestaurants(userData): Observable<any> {
    const endpoint = API_URL + 'user/get_nearby/';
    const userObject = {
      email: userData.email
    };
    return this.http.get(endpoint, { params: userObject });
  }
}