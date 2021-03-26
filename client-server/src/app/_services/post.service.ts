import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = '/api';
const POST_API = AUTH_API + '/restaurant/post/'

@Injectable({
  providedIn: 'root'
})
export class PostService {

  constructor(private http: HttpClient) { }

  /*
  @Input: None
  @Output: List of all posts by a restaurant

  Retrieves all posts from restaurant in the database using restaurant id.
  */
  getRestaurantPosts(): Observable<any> {
    const endpoint = POST_API;
    return this.http.get(endpoint);
  }

  /*
  @Input: JSON object restaurant_id, user_email, and content
  @Output: None

  Creates a post on the for the restaurant on their timeline.
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
