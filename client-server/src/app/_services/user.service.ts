import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = '/api/'
const SDUSER_ENDPOINT = API_URL + 'user/';
const SUBSCRIBER_ENDPOINT = API_URL + 'subscriber/';
const NLUSER_ENDPOINT = API_URL + 'newsletter/';

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
  private static readonly NLUSER_ENDPOINT = '/newsletter';



  /**
   * a get request to Django that has a template containing csrf token will set the token in the cookie
   * this is needed for Django to handle api calls from the browser
   * @returns a response object from the Django server
   */
  setCSRFToken(): Observable<any> {
    return this.http.get(API_URL + 'admin', { responseType: 'text' });
  }

  /**
   * Modifies an sduser
   * 
   * @param userData - JSON object containing fields to be modified for an sduser:
   *                    Required fields:
   *                     profile_id (string)
   * @returns JSON object representing the updated sduser
   */
  editAccountUser(userData): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + 'edit/'
    return this.http.put<any>(endpoint, userData, httpOptions);
  }

  /**
   * Creates a new subscriber profile for the sduser
   * 
   * @param userData - JSON object containing:
   *                     first_name (string),
   *                     last_name (string),
   *                     postalCode (string),
   *                     phone (number)
   * @returns JSON object representing the newly made subscriber profile
   */
  createSubscriberProfile(userData): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'signup/'
    return this.http.post<any>(endpoint, userData, httpOptions);
  }

  /**
   * Modifies an existing subscriber profile
   * 
   * @param userData - JSON object containing:
   *                     first_name (string),
   *                     last_name (string),
   *                     postalCode (string),
   *                     phone (number)
   * @returns JSON object representing the updated subscriber profile
   */
  editSubscriberProfile(userData): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'profile/';
    return this.http.put<any>(endpoint, userData, httpOptions);
  }

  /**
   * Retrieves the subscriber profile of a user
   * @returns JSON object representing the obtained subscriber profile
   */
  getSubscriberProfile(): Observable<any> {
    const endpoint = SUBSCRIBER_ENDPOINT + 'profile/'
    return this.http.get(endpoint);
  }

  /**
   * Deacivates the user's account (does not delete user from the database)
   * @param id - user_id of the sduser
   * @returns message from the Django server (success or fail with errors)
   */
  deactivateUser(id: string): Observable<any> {
    const endpoint = API_URL + 'user/deactivate/';
    return this.http.post<any>(endpoint, JSON.stringify({ 'id': id }), httpOptions);
  }

  /**
   * Changes the user's password
   * (a new access token is returned and the
   * refresh token in the cookie is also updated)
   * 
   * @param passwordData - JSON object containing:
   *                        old_password (string),
   *                        new_password1 (string),
   *                        new_password2 (string)
   * @returns Observable from password change request
   * (either containing a new access token or messages
   * indicating the errors)
   */
  changeUserPassword(passwordData: any): Observable<any> {
    const endpoint = API_URL + 'user/change_password/';
    return this.http.post<any>(endpoint, passwordData, httpOptions);
  }

  /**
   * Adds a new restaurant to the user's favourites list
   * 
   * @param data - JSON object containing:
   *                restaurant_id (string)
   * @returns successful message or an error
   */
  addFavouriteRestaurant(data): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `favourite/`
    return this.http.post<any>(endpoint, data)
  }

  /**
   * Retrieves all restaurants favourited by the user
   * @returns list of JSON objects representing restaurants
   */
  getFavouriteRestaurants(): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `favourite/`
    return this.http.get(endpoint)
  }

  /**
   * Removes a restaurant from the user's favourites list
   * 
   * @param restaurant_id - id of the restaurant to be
   *  removed from the user's favourites list
   * @returns successful message or an error
   */
  removeFavRestaurant(restaurant_id): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `favourite/${restaurant_id}/`
    return this.http.delete<any>(endpoint)
  }

  /**
   * Retrieves a list of up to 5 JSON objects, each one contains
   * the restaurant object and the distance from the user
   * @returns list of JSON objects (max up to 5)
   */
  getNearbyRestaurants(): Observable<any> {
    const endpoint = SDUSER_ENDPOINT + `nearby/`
    return this.http.get(endpoint);
  }

 /**
  * Insert a newsletter user into the db
  * @param userData - JSON user object
  * @returns Observable containing a user object or error
  */
  newsletterSignup(userData): Observable<any> {
    const endpoint = NLUSER_ENDPOINT + `signup/`;
    return this.http.post<any>(endpoint, userData);
  }

}
