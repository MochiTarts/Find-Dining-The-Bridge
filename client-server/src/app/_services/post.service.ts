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

  /*
  @Input: None
  @Output: List of all posts by a restaurant

  Retrieves all posts from a restaurant in the database (for RO).
  */
  getRestaurantPosts(): Observable<any> {
    const endpoint = POST_API;
    return this.http.get(endpoint);
  }

  /*
  @Input: restaurant_id
  @Output: List of all posts by a restaurant

  Retrieves all posts from a restaurant in the database (for public and BU user).
  */
  getRestaurantPostsById(restaurant_id): Observable<any> {
    const endpoint = PUBLIC_POST_API + `${restaurant_id}/`;
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object containing:
            restaurant_id (string),
            content (string; max_length=4096)
  @Output: JSON object of inserted post record

  Inserts a new restaurant post into the database
  */
  createPost(postInfo): Observable<any> {
    const endpoint = POST_API;
    return this.http.post<any>(endpoint, postInfo);
  }

  /*
  @Input: Post id of the post to be deleted
  @Output: None

  Deletes a post using post id.
  */
  deletePost(postId): void {
    const endpoint = POST_API + postId + '/';
    this.http.delete<any>(endpoint).subscribe((data) => {});
  }
}
