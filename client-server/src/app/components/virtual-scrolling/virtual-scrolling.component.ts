import { Component, OnInit, ChangeDetectionStrategy, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
// import { TimelineService } from 'src/app/service/timeline.service';
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
    // private authFirebase: FirebaseAuthService,
    private route: ActivatedRoute,
    // private timeline: TimelineService,
  ) { }

  ngOnInit(): void {
    // this.authFirebase.userProfile.subscribe((user) => {
    //   this.restaurantId = this.route.snapshot.queryParams.restaurantId || user.restaurantId;
    //   this.loadTimeline(this.restaurantId);
    // })
  }

  loadTimeline(id) {
    // this.timeline.getRestaurantPosts(id).subscribe((data) => {
    //   this.posts = data.Posts;
    //   this.lstPosts.next(this.posts);
    // });
  }

}
