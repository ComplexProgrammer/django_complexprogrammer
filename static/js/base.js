var app = angular.module("App", []);
app.filter('jsonDate', ['$filter', function ($filter) {
    return function (input, format) {
        return (input)
            ? $filter('date')(parseInt(input.substr(6)), format)
            : '';
    };
}]);
app.controller("Base", ["$scope", "$window", "$http", "$filter", function ($scope, $window, $http, $filter) {
    $scope.login="Login";
    $scope.clickLogin = function(){
        myModal.show();
    }
    $scope.user=checkAuth();
    if($scope.user!=false){
        $scope.login=checkUserName();
    }
    function getContacts(){
        $http({
            method: 'POST',
            url: "/getUser?uid="+$scope.user.uid+"&not_me=1",
        }).then(function (d) {
            console.log(d.data);
            $scope.Contacts = d.data;
        }, function (error) {
            console.log("error in getUser -> ", error);
        });
    }
    function getCountNewMessages(){
        $http({
            method: 'POST',
            url: "/getCountNewMessages?user_id="+$scope.user.id,
        }).then(function (d) {
            $scope.CountNewMessages = d.data;
        }, function (error) {
            console.log("error in getCountNewMessages -> ", error);
        });
    }
    function getChatUserRelations(){
        $http({
            method: 'POST',
            url: "/getChatUserRelations?user_id="+$scope.user.id,
        }).then(function (d) {
            $scope.ChatUserRelations = d.data;
        }, function (error) {
            console.log("error in getChatUserRelations -> ", error);
        });
    }
    function getMyContacts(){
        $http({
            method: 'POST',
            url: "/getMyContacts?user_id="+$scope.user.id,
        }).then(function (d) {
            console.log(d.data);
            $scope.MyContacts = d.data;
        }, function (error) {
            console.log("error in getMyContacts -> ", error);
        });
    }
    $scope.loadContacts = function(){
        if($scope.MyContacts==null){
            getMyContacts()
        }
    }
    $scope.loadChats = function(){
        getChatUserRelations()
    }
    function loadMessageByContactId(receiver_id){
        $http({
            method: 'POST',
            url: "/getChatMessages?receiver_id="+receiver_id+"&sender_id="+$scope.user.id,
        }).then(function (d) {
            console.log(d.data);
            $scope.Messages = d.data;
        }, function (error) {
            console.log("error in getChatMessages -> ", error);
        });
    }
    $scope.loadMessageByContactId = function(receiver_id, index, count){
        $scope.is_chat=0
        $scope.is_contact=1
        $scope.receiver_id=receiver_id
        for(i=0;i<count;i++){
           document.getElementById("contact"+i).className = "friend-drawer--onhover";
        }
        document.getElementById("contact"+index).className = "active";
        $scope.selectedUser=$scope.MyContacts.filter(user => user.id == receiver_id)[0]
        console.log($scope.selectedUser)
        document.getElementById('contactsArea').style.display = "none"
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
        loadMessageByContactId(receiver_id)
    }
    var socket;
    $(document).ready(function(){

    });
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('join', {});
    });
    socket.on('status', function(data) {
        if(data.active){
//            alertify.success(data.text);
        }
        else{
            alertify.error(data.text);
        }
    });
    socket.on('message', function(data) {
        console.log($scope.Messages)
        console.log(data)
        if($scope.Messages != "undefined" && $scope.Messages != null){
            $scope.Messages = $scope.Messages.concat(data);
            console.log($scope.Messages);
        }
        if($scope.user.id==data.sender_id){

        }
        else{
            refreshMessages()
//            alertify.success(data.text)
        }
//        if(chat_id>0){
//            let msg_card_body = document.querySelector('#msg_card_body');
//            let msg_time_span = document.createElement('span');
//            let msg_container_div = document.createElement('div');
//            let img = document.createElement('img');
//            let img_cont_msg_div = document.createElement('div');
//            let div = document.createElement('div');
//
//            if($scope.user.id==data.sender_id){
//                img.setAttribute('class', 'rounded-circle user_img_msg');
//                img.setAttribute('ng-show', $scope.user.photo_url);
//                img.setAttribute('src', $scope.user.photo_url);
//                img_cont_msg_div.setAttribute('class', 'img_cont_msg');
//                img_cont_msg_div.appendChild(img);
//                msg_time_span.setAttribute('class', 'msg_time_send');
//                msg_time_span.append(new Date());
//                msg_container_div.setAttribute('class', 'msg_cotainer_send');
//                msg_container_div.append(data.text);
//                msg_container_div.append(msg_time_span);
//                div.setAttribute('class', 'd-flex justify-content-end mb-4');
//                div.appendChild(msg_container_div);
//                div.appendChild(img_cont_msg_div);
//            }
//            else{
//                img.setAttribute('class', 'rounded-circle user_img_msg');
//                img.setAttribute('ng-show', $scope.selectedUser.photo_url);
//                img.setAttribute('src', $scope.selectedUser.photo_url);
//                img_cont_msg_div.setAttribute('class', 'img_cont_msg');
//                img_cont_msg_div.appendChild(img);
//                msg_time_span.setAttribute('class', 'msg_time');
//                msg_time_span.append(new Date());
//                msg_container_div.setAttribute('class', 'msg_cotainer');
//                msg_container_div.append(data.text);
//                msg_container_div.append(msg_time_span);
//                div.setAttribute('class', 'd-flex justify-content-start mb-4');
//                div.appendChild(img_cont_msg_div);
//                div.appendChild(msg_container_div);
//                alertify.success(data.text)
//            }
//            msg_card_body.append(div);
//        }
//            $('#chat').val($('#chat').val() + data.text + '\n');
//            $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    function refreshMessages(){
        alertify.success('Sizga yangi xabar keldi')
    }
    function sendMessage(){
        $scope.model={
            sender_id:$scope.user.id,
            receiver_id:$scope.receiver_id,
            text:$scope.text
        }
        console.log($scope.model)
        $http({
            method: 'POST',
            url: "/sendMessage",
            data: JSON.stringify($scope.model),
            dataType: "json"
        }).then(function (d) {
            console.log(d.data);
            $scope.text=''
//            if($scope.is_chat==1){
//                loadMessageByChatId(d.data[0].chat_id)
//            }
//            if($scope.is_contact==1){
//                loadMessageByContactId($scope.receiver_id)
//            }
        }, function (error) {
            console.log("error in sendMessage -> ", error);
        });
//        text = $('#messageText').val();
//        $('#messageText').val('');
//        socket.emit('text', {msg: text});
    }
//    $('#send').click(function(e) {
//        sendMessage();
//    });
    $('#messageText').keyup(function(e){
        if(e.keyCode == 13)
        {
            sendMessage();
        }
    });
    $window.join_room = function() {
        myModal.hide();
        socket.emit('join', {});
        $scope.user=checkAuth();
        if($scope.user!=false){
            $scope.login=checkUserName();
        }
        getMyContacts()
        for(i=0;i<document.getElementsByClassName('friend-drawer selected_user').length;i++){
           document.getElementsByClassName('friend-drawer selected_user')[i].className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("myForm").style.display = "block";
        document.getElementById("openChatBtn").style.display = "none";
    };
    $window.leave_room = function() {
        $scope.user=checkAuth();
        $scope.login="Login";
        document.getElementById("myForm").style.display = "none";
	    document.getElementById("openChatBtn").style.display = "block";
        myModal.hide();
        socket.emit('left', {});
    };
    $scope.openForm = function() {
        getCountNewMessages()
        if($scope.login=="Login"){
            myModal.show();
        }
        else{
            if($scope.MyContacts==null){
                getMyContacts()
            }
            for(i=0;i<document.getElementsByClassName('friend-drawer selected_user').length;i++){
               document.getElementsByClassName('friend-drawer selected_user')[i].className = "friend-drawer friend-drawer--onhover";
            }
            document.getElementById("myForm").style.display = "block";
            document.getElementById("openChatBtn").style.display = "none";
        }
    }
    $scope.closeForm = function() {
	  document.getElementById("myForm").style.display = "none";
	  document.getElementById("openChatBtn").style.display = "block";
	}
	$scope.closeMessageArea = function(){
	    document.getElementById('messageTextArea').style.display = "none"
        document.getElementById('contactsArea').style.display = "block"
	}
    function loadMessageByChatId(chat_id){
        $http({
            method: 'POST',
            url: "/getChatMessagesByChatId?chat_id="+chat_id,
        }).then(function (d) {
            console.log(d.data);
            $scope.Messages = d.data;
        }, function (error) {
            console.log("error in getChatMessagesByChatId -> ", error);
        });
    }
    $scope.loadMessageByChatId = function(receiver_id, chat_id, index, count){
        $scope.is_chat=1
        $scope.is_contact=0
        $scope.receiver_id=receiver_id
        for(i=0;i<count;i++){
           document.getElementById("user"+i).className = "friend-drawer friend-drawer--onhover";
        }
        document.getElementById("user"+index).className = "friend-drawer selected_user";
        $scope.selectedUser=$scope.ChatUserRelations.filter(user => user.user_id == receiver_id)[0].user
        console.log($scope.selectedUser)
        document.getElementById('contactsArea').style.display = "none"
        document.getElementById('messageTextArea').style.display = "block"
        $(".chat-bubble").hide("slow").show("slow");
        loadMessageByChatId(chat_id)
    }
    $scope.sendMessage=function(){
        sendMessage()
    }

}]);