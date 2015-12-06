from flask import render_template, jsonify, request
from flask.ext.restful import reqparse, abort, Api, Resource 
from application.api import api 
from models import AO3data, AO3url

version_base = '/v1.0'
a = Api(api, prefix=version_base)

# Arguments
parser = reqparse.RequestParser()
parser.add_argument("type", type=str)
parser.add_argument("tag_id", type=str, required=True, help="A tag must be specified!")
parser.add_argument("page", type=int)
parser.add_argument("sort_direction", type=str)
parser.add_argument("query", type=str)
parser.add_argument("title", type=str)
parser.add_argument("creator", type=str)
parser.add_argument("revised_at", type=str)
parser.add_argument("complete", type=int)
parser.add_argument("single_chapter", type=int)
parser.add_argument("sort_column", type=str)
parser.add_argument("rating_ids", type=int, action="append")
parser.add_argument("warning_ids", type=int, action="append")
parser.add_argument("category_ids", type=int, action="append")
parser.add_argument("fandom_names", type=str, action="append")
parser.add_argument("fandom_ids", type=int, action="append")
parser.add_argument("character_names", type=str, action="append")
parser.add_argument("character_ids", type=int, action="append")
parser.add_argument("relationship_names", type=str, action="append")
parser.add_argument("relationship_ids", type=int, action="append")
parser.add_argument("freeform_names", type=str, action="append")
parser.add_argument("freeform_ids", type=int, action="append")
parser.add_argument("other_tag_names", type=str, action="append")
parser.add_argument("other_tag_ids", type=int, action="append")
parser.add_argument("word_count", type=str)
parser.add_argument("hits", type=str)
parser.add_argument("kudos_count", type=str)
parser.add_argument("comments_count", type=str)
parser.add_argument("bookmarks_count", type=str)

class Stats(Resource):
  
  # Stats for any search filter
  def get(self):
    # Returns stats for any list of search arguments
    # print "-------------------------"
    # print "======= NEW CYCLE ======="
    s = AO3data(request.url)
    url = AO3url()
    url.setFilters(parser.parse_args())
    return s.getTopInfo(url.getUrl())

class TagStats(Resource):

  # Stats for just a given tag id
  def get(self, tag_id):
    # todo: possibly remove completely? possibly unnecessary?
    # todo: add error handling for empty tagid
    params = {
      "type": "works",
      "params": {
        "tag_id": tag_id
      } 
    }
    s = AO3data()
    url = AO3url().getUrl(params) 
    return s.getTopInfo(url)

# API routing
a.add_resource(Stats, "/stats")
a.add_resource(TagStats, "/stats/tag/<string:tag_id>")
