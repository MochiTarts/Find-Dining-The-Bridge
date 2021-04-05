import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArticleSingleCardComponent } from './article-single-card.component';

describe('ArticleSingleCardComponent', () => {
  let component: ArticleSingleCardComponent;
  let fixture: ComponentFixture<ArticleSingleCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArticleSingleCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArticleSingleCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
