var Home = {
  name: 'Home',
  template: '#component_home'
}

var BucketDetail = {
  name: 'BucketDetail',
  template: '#component_bucket_detail',
  props: {
    'bucket_filter': { type: String },
    'bucketName': { type: String },
    'page': { default: 1 }
  },
  watch: {
    // call again the method if the route changes
    '$route': 'updateAssetsFromRoute',
    'bucket_search_input': 'updateAssetsFromSearchInput'
  },
  data: function() {
    return {
      bucket_objs: [],
      bucket_meta: {},
      bucket_search_input: '' ,
    }
  },
  computed: {
    current_bucket_name: function () {
      if (this.bucket_objs.length > 0) {
        return this.bucket_objs[0].bucket.name
      } else {
        return "";
      }
    },
    current_bucket_id: function () {
      if (this.bucket_objs.length > 0) {
        return this.bucket_objs[0].bucket.id
      } else {
        return null;
      }
    },
    has_next_page: function() {
      return this.bucket_meta.next != null;
    },
    next_page_num: function() {
      return this.bucket_meta.next;
    },
    has_prev_page: function() {
      return this.bucket_meta.previous != null;
    },
    prev_page_num: function() {
      return this.bucket_meta.previous;
    }
  },
  methods: {
    fetchAssetsListByBucketName: function(bucketName, searchTerm) {
      this.bucket_objs = [];
      var self = this;
      var page = this.$route.params.page;
      var bucket = encodeURI(bucketName);
      var querystring = 'django_ct:assets_manager.asset AND bucket:"' + bucket + '"';
      var bucket_list_url = "/api/v1/asset/search/?page=" + page + "&q=" + querystring;
      if (searchTerm) {
        bucket_list_url += encodeURI(" AND " + searchTerm);
      }
      $.getJSON(
        bucket_list_url,
        function(json, textStatus) {
          self.bucket_objs = json.objects;
          self.bucket_meta = json.meta;
      });
    },
    updateAssetsFromRoute: function() {
      var route_bucketName = this.$route.params.bucketName;
      this.fetchAssetsListByBucketName(route_bucketName);
    },
    updateAssetsFromSearchInput: function() {
      var route_bucketName = this.$route.params.bucketName;
      var search_term = this.bucket_search_input;

      this.fetchAssetsListByBucketName(route_bucketName, search_term);
    },
    formatDate: function(dateString) {
      /* dependência moment.js */
      return moment(dateString, "YYYY-MM-DDTHH:mm:ss.SSSSSS").format("YYYY-MM-DD HH:mm:ss");
    }
  },
  created: function() {
    this.updateAssetsFromRoute();
  },
}

var app_router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      props: true
    },
    {
      path: '/buckets/:bucketName/page/:page',
      name: 'buckets_details',
      component: BucketDetail,
      props: true
    }
  ]
})

var main_app = new Vue({
  el: '#vueapp',
  router: app_router,
  data: {
    sidebar_buckets: [],
    bucket_filter: ''
  },
  mounted: function(){
    this.fetchBucketList();
  },
  methods: {
    fetchBucketList: function(){
      var self = this;
      var bucket_list_url = "/api/v1/asset_bucket/search/";
      if (this.bucket_filter !== ""){
        bucket_list_url += "?q=*" + this.bucket_filter + "*";
      }
      $.getJSON(
        bucket_list_url,
        function(json, textStatus) {
          self.sidebar_buckets = json.objects
      });
    }
  },
  watch: {
    // whenever question changes, this function will run
    bucket_filter: function () {
      this.fetchBucketList();
    }
  },
})
