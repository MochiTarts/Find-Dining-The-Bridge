import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';
import { ArticleService } from '../../_services/article.service';

@Component({
  selector: 'app-article-headline-card',
  templateUrl: './article-headline-card.component.html',
  styleUrls: ['./article-headline-card.component.scss']
})
export class ArticleHeadlineCardComponent implements OnInit {
  @Input() article: any;

  @Output() articleOutput: EventEmitter<any> = new EventEmitter<any>();

  articleTextPreview: string = "";

  constructor(
    private userService: UserService,
    private tokenStorage: TokenStorageService,
    private articleService: ArticleService,
  ) { }

  ngOnInit(): void {
    var temp = document.createElement("span");
    temp.innerHTML = this.article.content;
    this.articleTextPreview = temp.textContent || temp.innerText || "";
  }

  openArticle() {
    //this.articleService.openArticle(this.article);
    this.articleOutput.emit(this.article);
  }

}
