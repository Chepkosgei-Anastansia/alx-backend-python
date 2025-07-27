from rest_framework import permissions
from chats.models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to users who are participants in the conversation.
    """
    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        
        if isinstance(obj, Conversation):
            return request.user in obj.conversation.participants.all()
        elif isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        return False


class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only if the user is in the conversation related to the message.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        return request.user in obj.conversation.participants.all()
    
class IsConversationOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        return obj.participants.filter(user_id=request.user.user_id).exists()