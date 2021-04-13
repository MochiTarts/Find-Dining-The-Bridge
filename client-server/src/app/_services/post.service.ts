import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = '/api';
const POST_API = AUTH_API + '/restaurant/post/'
const PUBLIC_POST_API = AUTH_API + '/restaurant/public/post/'

@Injectable({
  providedIn: 'root'
})
export class PostService {

  constructor(private http: HttpClient) { }

  /**
   * Retrieves all posts from a restaurant in the database (for RO)
   * @returns list of all posts by a restaurant
   */
  getRestaurantPosts(): Observable<any> {
    const endpoint = POST_API;
    return this.http.get(endpoint);
  }

  /**
   * Retrieves all posts from a restaurant in the database (for public and BU user)
   * 
   * @param restaurant_id - the restaurant's id
   * @returns list of all posts by a restaurant
   */
  getRestaurantPostsById(restaurant_id): Observable<any> {
    const endpoint = PUBLIC_POST_API + `${restaurant_id}/`;
    return this.http.get(endpoint);
  }

  /**
   * Inserts a new restaurant post into the database
   * 
   * @param postInfo - JSON object containing:
   *                    restaurant_id (string),
   *                    content (string; max_length=4096)
   * @returns JSON object of the inserted post record
   */
  createPost(postInfo): Observable<any> {
    const endpoint = POST_API;
    return this.http.post<any>(endpoint, postInfo);
  }

  /**
   * Deletes a post given its post id
   * @param postId - post id of the post to be deleted
   */
  deletePost(postId): void {
    const endpoint = POST_API + postId + '/';
    this.http.delete<any>(endpoint).subscribe((data) => {});
  }
  
}
