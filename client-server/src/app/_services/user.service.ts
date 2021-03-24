import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = '/api/'
const SDUSER_ENDPOINT = '/api/user/';
const SUBSCRIBER_ENDPOINT = '/api/subscriber/';
const OWNER_ENDPOINT = '/api/owner/';
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
  @Input: JSON object containing fields to be modified for an sduser
  @Ouput: JSON object representing the updated sduser
  Modified an sduser
  */
  editAccountUser(userData): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + 'edit/'
    return this.http.put<any>(endpoint, userData, httpOptions);
  }

  /*
  @Input: JSON object containing required fields for making a subscriber profile
  @Output: JSON object representing the created subscriber profile
  Makes a new subscriber profile
  */
  createSubscriberProfile(userData): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'signup/'
    return this.http.post<any>(endpoint, userData, httpOptions);
  }

  /*
  @Input: JSON object containing user email and fields of subscriber profile to be modified
  @Output: JSON object representing the updated subscriber profile
  Modifies an existing subscriber profile
  */
  editSubscriberProfile(userData): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'profile/';
    return this.http.put<any>(endpoint, userData, httpOptions);
  }

  /*
  @Input: the logged in user's user_id from their token
  @Output: Return all fields of a subscriber
  Get all fields of subscriber
  */
  getSubscriberProfile(): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'profile/'
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object containing userID and fields of subscriber profile to be modified
  @Output: JSON object representing the updated subscriber profile
  Edit consumer's consent status
  */
  editConsentStatus(userData): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'consent_status/';
    return this.http.put<any>(endpoint, userData, httpOptions);
  }

  /*
  @Input: JSON object containing restaurant_id of restaurant that will be part of this new relation
  @Input: user_id of the user who will be part of this new relation
  @Output: Message from request or error
  Add a new restaurant to a user's list of favourites
  */
  addFavouriteRestaurant(data, user_id): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `/${user_id}/favourite/`
    return this.http.post<any>(endpoint, data)
  }

  /*
  @Input: user_id of user whose list of favourites will be retrieved
  @Output: List of favourited restaurants
  Get all restaurants favourited by a user
  */
  getFavouriteRestaurants(user_id): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `/${user_id}/favourite/`
    return this.http.get(endpoint)
  }

  /*
  @Input: JSON user-restaurant favourite object
  @Output: Message from request
  Removes a restaurant from a user's list of favourites
  */
  removeFavRestaurant(user_id, restaurant_id): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `/${user_id}/favourite/${restaurant_id}/`
    return this.http.delete<any>(endpoint)
  }

  /*
  @Input: user_id of the subscriber user
  @Output: list of nearby restaurants from the subscriber user
  Returns a list of up to 5 json objects, each object contains
  the restaurant_id and the distance from the subscriber
  List is ordered from nearest to furthest
  */
  getNearbyRestaurantsSubscriber(user_id): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + `/nearby/${user_id}/`
    return this.http.get(endpoint);
  }

  /*
  @Input: user_id of the restaurant owner user
  @Output: list of nearby restaurants from the restaurant owner
  Returns a list of up to 5 json objects, each object contains
  the restaurant_id and the distance from the restaurant owner
  List is ordered from nearest to furthest
  */
  getNearbyRestaurantsOwner(user_id): Observable<any> {
    const endpoint = OWNER_ENDPOINT + `/nearby/${user_id}/`;
    return this.http.get(endpoint);
  }

  /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */
  /*
  BELOW ARE THE OLD SERVICE METHODS FROM PREVIOUS REPO
  SOME CAN BE MOVED OVER, SOME CAN BE SCRAPPED
  */
  /* ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

  /*
  @Input: JSON object from auth
  @Output: Return all fields of a user
  Get all fields of a user
  */
  getConsumer(userData): Observable<any> {
    const endpoint = API_URL + 'consumer_subscriber_data/';
    const userObject = {
      email: userData.email
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
      email: userData.email
    };
    return this.http.get(endpoint, { params: userObject });
  }


  editConsumer(userData): Observable<any> {
    const endpoint = API_URL + 'consumer_subscriber_edit/';
    return this.http.post<any>(endpoint, userData);
  }


  editOwner(userData): Observable<any> {
    const endpoint = API_URL + 'restaurant_owner_edit/';
    return this.http.post<any>(endpoint, userData);
  }


  /*
  @Input: JSON object from auth
  @Output: Return True if user is in database, False otherwise
  Check if user exists in the database
  */
  editUser(userData): Observable<any> {
    const endpoint = API_URL + 'edit/';

    return this.http.post<any>(endpoint, userData);
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
  @Input: None
  @Output: None
  Deactivate the user account
  */
  deactivateUser(id: string): Observable<any> {
    const endpoint = API_URL + 'user/deactivate/';
    return this.http.post<any>(endpoint, JSON.stringify({ 'id': id }), httpOptions);
  }

  getNearbyRestaurants(userData): Observable<any> {
    const endpoint = API_URL + 'user/get_nearby/';
    const userObject = {
      email: userData.email
    };
    return this.http.get(endpoint, { params: userObject });
  }

}