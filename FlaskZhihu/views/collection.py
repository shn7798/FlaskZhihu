# -*- coding: utf-8 -*-
__author__ = 'shn7798'

from flask import url_for, abort, redirect, render_template, request
from flask.ext.classy import FlaskView, route
from flask.ext.login import current_user, login_required

from FlaskZhihu.extensions import db
from FlaskZhihu.forms import CollectionAddForm, CollectionEditForm
from FlaskZhihu.models import Answer, Question, User, Collection
from FlaskZhihu import signals
from FlaskZhihu.helpers import keep_next_url

__all__ = ['CollectionView']


class CollectionView(FlaskView):
    route_base = '/collection'

    @route(r'/<int:id>/')
    def show(self, id):
        collection = Collection.query.options(db.joinedload(Collection.answers)).get_or_404(id)
        return render_template('collection/show.html', collection=collection)

    @route(r'/add/', methods=['GET', 'POST'])
    @login_required
    def add(self):
        form = CollectionAddForm()
        if form.validate_on_submit():
            collection = Collection()
            collection.user = current_user
            collection.title = form.title.data
            collection.description = form.description.data

            db.session.add(collection)
            db.session.commit()

            return redirect(url_for('CollectionView:my'))

        return render_template('collection/add.html', form=form)

    @route(r'/<int:id>/delete/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def delete(self, id, next_url=None):
        collection = Collection.query.filter(
            db.and_(
                Collection.id == id,
                Collection.user_id == current_user.id,
            )
        ).first_or_404()

        collection.answers = []
        db.session.delete(collection)
        db.session.commit()
        signals.collection_answer_delete.send(collection)
        return redirect(next_url or url_for('CollectionView:my'))


    @route(r'/<int:id>/edit/', methods=['GET', 'POST'])
    @login_required
    def edit(self, id):
        collection = Collection.query.filter(
            db.and_(
                Collection.id == id,
                Collection.user_id == current_user.id
            )
        ).first_or_404()

        form = CollectionEditForm()

        if form.validate_on_submit():
            if form.title.data:
                collection.title = form.title.data
            if form.description.data:
                collection.description = form.description.data

            db.session.commit()
            return redirect(url_for('CollectionView:show', id=collection.id))
        else:
            form.title.data = collection.title
            form.description.data = collection.description
            return render_template('collection/edit.html', form=form)


    @route(r'/my/')
    @login_required
    def my(self):
        collections = current_user.collections
        return render_template('collection/my.html', collections=collections)


    @route(r'/<int:id>/answer/<int:answer_id>/add/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def add_answer(self, id, answer_id, next_url=None):
        collection = Collection.query.filter(
            db.and_(
                Collection.id == id,
                Collection.user_id == current_user.id
            )
        ).first_or_404()
        answer = Answer.query.get_or_404(answer_id)
        collection.answers.append(answer)
        db.session.commit()

        signals.collection_answer_add.send(collection)
        return redirect(next_url or url_for('CollectionView:show', id=collection.id))


    @route(r'/<int:id>/answer/<int:answer_id>/delete/', methods=['GET', 'POST'])
    @login_required
    @keep_next_url
    def delete_answer(self, id, answer_id, next_url=None):
        collection = Collection.query.filter(
            db.and_(
                Collection.id == id,
                Collection.user_id == current_user.id
            )
        ).first_or_404()
        answer = Answer.query.get_or_404(answer_id)
        collection.answers.remove(answer)
        db.session.commit()

        signals.collection_answer_delete.send(collection)
        return redirect(next_url or url_for('CollectionView:show', id=collection.id))


    @route(r'/select/by/answer/<int:answer_id>/')
    @login_required
    @keep_next_url
    def select_by_answer(self, answer_id, next_url=None):
        collections = current_user.collections
        return render_template('collection/select_by_answer.html', collections=collections, answer_id=answer_id)