import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { PostService } from 'src/app/_services/post.service';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-virtual-scrolling',
  templateUrl: './virtual-scrolling.component.html',
  styleUrls: ['./virtual-scrolling.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class VirtualScrollingComponent implements OnInit {
  @Input() restaurantName: string = '';

  restaurantId: string = '';

  posts: any[] = [];
  lstPosts = new BehaviorSubject<any[]>(null);

  constructor(
    private postService: PostService,
  ) { }

  ngOnInit(): void {
    this.loadPosts();
  }

  loadPosts() {
    this.postService.getRestaurantPosts().subscribe((data) => {
      this.posts = data.Posts;
      this.lstPosts.next(this.posts);
    })
  }

}
