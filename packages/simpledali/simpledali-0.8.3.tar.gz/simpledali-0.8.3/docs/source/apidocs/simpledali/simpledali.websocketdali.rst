:py:mod:`simpledali.websocketdali`
==================================

.. py:module:: simpledali.websocketdali

.. autodoc2-docstring:: simpledali.websocketdali
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`WebSocketDataLink <simpledali.websocketdali.WebSocketDataLink>`
     - .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink
          :summary:

API
~~~

.. py:class:: WebSocketDataLink(uri, packet_size=-1, dlproto=DLPROTO_1_0, verbose=False, ping_interval=None)
   :canonical: simpledali.websocketdali.WebSocketDataLink

   Bases: :py:obj:`simpledali.abstractdali.DataLink`

   .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink

   .. rubric:: Initialization

   .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink.__init__

   .. py:method:: createDaliConnection()
      :canonical: simpledali.websocketdali.WebSocketDataLink.createDaliConnection
      :async:

      .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink.createDaliConnection

   .. py:method:: send(header, data)
      :canonical: simpledali.websocketdali.WebSocketDataLink.send
      :async:

      .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink.send

   .. py:method:: parseResponse()
      :canonical: simpledali.websocketdali.WebSocketDataLink.parseResponse
      :async:

      .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink.parseResponse

   .. py:method:: isClosed()
      :canonical: simpledali.websocketdali.WebSocketDataLink.isClosed

      .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink.isClosed

   .. py:method:: close()
      :canonical: simpledali.websocketdali.WebSocketDataLink.close
      :async:

   .. py:method:: _force_close()
      :canonical: simpledali.websocketdali.WebSocketDataLink._force_close

      .. autodoc2-docstring:: simpledali.websocketdali.WebSocketDataLink._force_close
