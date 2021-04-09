import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { TokenStorageService } from '../../_services/token-storage.service';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'app-article-common-card',
  templateUrl: './article-common-card.component.html',
  styleUrls: ['./article-common-card.component.scss']
})
export class ArticleCommonCardComponent implements OnInit {
  @Input() article: any;

  @Output() articleOutput: EventEmitter<any> = new EventEmitter<any>();

  articleTextPreview: string = "";

  constructor(
    private userService: UserService,
    private tokenStorage: TokenStorageService,
  ) { }

  ngOnInit(): void {
    var temp = document.createElement("span");
    temp.innerHTML = this.article.content;
    this.articleTextPreview = temp.textContent || temp.innerText || "";
  }

  openArticle() {
    this.articleOutput.emit(this.article);
  }

}
