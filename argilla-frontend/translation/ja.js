export default {
  multi_label_selection: "マルチラベル",
  ranking: "ランキング",
  label_selection: "ラベル",
  span: "範囲選択",
  text: "テキスト",
  chat: "チャット",
  image: "画像",
  rating: "レーティング",
  minimize: "最小化",
  select: "選択",
  search: "検索",
  searchPlaceholder: "クエリを入力",
  searchDatasets: "データセットを検索",
  share: "進捗を共有",
  expand: "拡大",
  copied: "Copied",
  copiedToClipboard: "コピーしました",
  copyLink: "リンクをコピー",
  copyRecord: "レコードをコピー",
  refresh: "リフレッシュ",
  typeYourText: "テキストを入力",
  all: "すべて",
  value: "値",
  title: "タイトル",
  description: "説明",
  labels: "ラベル",
  order: "順番",
  owner: "オーナー",
  useMarkdown: "Markdownを使用",
  suggestionFirst: "提案を先頭に表示",
  visibleForAnnotators: "アノテーターに表示",
  recordInfo: "レコード情報",
  viewMetadata: "メタデータを見る",
  allowExtraMetadata: "追加メタデータを許可",
  extraMetadata: "追加メタデータ",
  dimension: "次元",
  visibleLabels: "デフォルトで表示するラベル数",
  annotationGuidelines: "アノテーションガイドライン",
  guidelines: "ガイドライン",
  taskDistribution: "タスク分配",
  minimumSubmittedResponses: "必要な最低回答数",
  taskDistributionTooltip:
    "タスクはすべてのレコードで最低回答数分\nの回答が提出されたときに完了となります",
  noAnnotationGuidelines:
    "このデータセットにはアノテーションガイドラインがありません",
  required: "必須",
  optional: "任意",
  template: "テンプレート",
  orgOrUsername: "組織・ユーザー名",
  hfToken: "Hugging Faceトークン",
  private: "プライベートにする",
  rows: "行",
  datasetName: "データセット名",
  noRecordsMessages: {
    datasetEmptyForAnnotator:
      "データセットは空です。管理者にレコードのアップロードを依頼してください。",
    datasetEmptyForAdmin:
      "データセットは空です。Python SDKを使用してレコードを追加できます。詳細は<a href='https://docs.argilla.io/latest/admin_guide/record/'>ドキュメント</a>を参照してください。",
    taskDistributionCompleted: "🎉 タスクは完了しています！",
    noSubmittedRecords: "まだ提出されたレコードはありません",
    noRecordsFound: "条件に一致する{status}レコードはありません",
    noRecords: "{status}レコードはありません",
    noPendingRecordsToAnnotate: "🎉 未アノテーションのレコードがなくなりました",
    noDraftRecordsToReview: "未提出の下書きはありません",
  },
  couldNotLoadImage: "画像の読み込みに失敗しました",
  breadcrumbs: {
    home: "ホーム",
    datasetSettings: "データセット設定",
    userSettings: "設定",
  },
  datasets: {
    left: "残り",
    completed: "完了済み",
    pending: "未回答",
  },
  recordStatus: {
    pending: "未回答",
    draft: "下書き",
    discarded: "回答放棄",
    submitted: "提出済み",
    validated: "検証済み",
    completedTooltip:
      "このレコードは完了しています。\n最小回答数が提出されました",
  },
  userSettings: {
    title: "設定",
    fields: {
      userName: "ユーザー名",
      firstName: "名",
      lastName: "姓",
      workspaces: "ワークスペース",
    },
    apiKey: "APIキー",
    apiKeyDescription:
      "APIキーを使うとPython SDKでデータセットを管理できます。",
    theme: "テーマ",
    language: "言語",
    copyKey: "コピー",
  },
  userAvatarTooltip: {
    settings: "設定",
    docs: "ドキュメンテーションを見る",
    logout: "ログアウト",
  },
  settings: {
    title: "データセット設定",
    datasetInfo: "データセット情報",
    seeYourDataset: "データセットを見る",
    editFields: "フィールドを編集",
    editQuestions: "質問を編集",
    editMetadata: "メタデータを編集",
    editVectors: "ベクトルを編集",
    deleteDataset: "データセットを削除",
    deleteWarning: "この操作は取り消せませんのでご注意ください",
    deleteConfirmation: "削除確認",
    deleteConfirmationMessage:
      "<strong>{workspaceName}</strong>からデータセット<strong>{datasetName}</strong>を削除します。この操作は取り消せません。",
    yesDelete: "はい、削除します",
    write: "Write",
    preview: "プレビュー",
    uiPreview: "UIプレビュー",
  },
  button: {
    ignore_and_continue: "無視して続ける",
    login: "サインイン",
    signin_with_provider: "{provider}でサインイン",
    "hf-login": "Hugging Faceでサインイン",
    sign_in_with_username: "ユーザー名でサインイン",
    cancel: "キャンセル",
    continue: "続ける",
    delete: "削除",
    exportToHub: "Push to Hub",
    tooltip: {
      copyToClipboard: "クリップボードにコピー",
      copyNameToClipboard: "データセット名をクリップボードにコピー",
      copyLinkToClipboard: "データセットリンクをクリップボードにコピー",
      goToDatasetSettings: "データセット設定に移動",
      datasetSettings: "データセット設定",
    },
  },
  to_submit_complete_required: "完了した回答を提出します",
  some_records_failed_to_annotate: "アノテーションに失敗したレコードがあります",
  changes_no_submit: "変更が提出されていません",
  bulkAnnotation: {
    recordsSelected:
      "1レコードが選択されています | {count}レコードが選択されています",
    recordsViewSettings: "レコードサイズ",
    fixedHeight: "レコードを折りたたむ",
    defaultHeight: "レコードを展開",
    to_annotate_record_bulk_required: "レコードが選択されていません",
    select_to_annotate: "すべて選択",
    pageSize: "ページサイズ",
    selectAllResults: "マッチした全{total}レコードを選択",
    haveSelectedRecords: "全{total}レコードが選択されました",
    actionConfirmation: "一括アクション確認",
    actionConfirmationText:
      "このアクションは{total}レコードに影響します。続行しますか？",
    allRecordsAnnotated: "{total}レコードが{action}されました",
    affectedAll: {
      submitted: "提出済み",
      discarded: "回答を放棄",
      draft: "下書きとして保存",
    },
  },
  shortcuts: {
    label: "ショートカット",
    pagination: {
      go_to_previous_record: "前 (←)",
      go_to_next_record: "次 (→)",
    },
  },
  questions_form: {
    validate: "検証",
    clear: "クリア",
    reset: "リセット",
    discard: "回答を放棄",
    submit: "提出",
    draft: "下書きとして保存",
    write: "記述",
  },
  sorting: {
    label: "並び替え",
    addOtherField: "+ フィールドを追加",
    suggestion: {
      score: "提案スコア",
      value: "提案された値",
    },
    response: "回答された値",
    record: "一般",
    metadata: "メタデータ",
  },
  suggestion: {
    agent: "\nエージェント: {agent}",
    score: "\nスコア: {score}",
    tooltip: "この質問には提案が含まれています: {agent} {score}",
    filter: {
      value: "提案された値",
      score: "スコア",
      agent: "エージェント",
    },
    plural: "提案",
    name: `提案`,
  },
  similarity: {
    "record-number": "レコード数",
    findSimilar: "類似文を探す",
    similarTo: "次の文と類似",
    similarityScore: "類似度",
    similarUsing: "類似度計算に使用:",
    expand: "拡大",
    collapse: "畳む",
  },
  spanAnnotation: {
    shortcutHelper: "文字単位で選択するには'Shift'を押し続けてください",
    notSupported: "範囲選択はご利用のブラウザではサポートされていません",
    searchLabels: "ラベルを検索",
  },
  login: {
    title: "サインイン",
    username: "ユーザー名",
    usernameDescription: "ユーザー名を入力",
    password: "パスワード",
    show: "表示",
    hide: "非表示",
    passwordDescription: "パスワードを入力",
    claim: "データは協働で。</br>モデルはさらなる高みへ。",
    error:
      "ユーザー名またはパスワードが間違っています。もう一度お試しください。",
    hf: {
      title: "{space}へようこそ",
      subtitle:
        "<strong>{user}</strong>さんと一緒にAI向けのデータセットを作成しましょう",
    },
  },
  of: "of",
  status: "ステータス",
  filters: "フィルター",
  filterBy: "キーワードで絞り込む",
  fields: "フィールド",
  field: "フィールド",
  questions: "質問",
  general: "一般",
  metadata: "メタデータ",
  vectors: "ベクトル",
  dangerZone: "危険ゾーン",
  responses: "回答",
  "reset-all": "すべてリセット",
  reset: "リセット",
  less: "Less",
  learnMore: "詳細",
  with: "with",
  find: "探す",
  cancel: "キャンセル",
  focus_mode: "集中モード",
  bulk_mode: "一括モード",
  update: "更新",
  youAreOnlineAgain: "オンラインになりました",
  youAreOffline: "オフラインです",
  write: "記述欄",
  preview: "プレビュー",
  metrics: {
    total: "合計",
    progress: {
      default: "進捗率",
      my: "あなたの進捗率",
      team: "チームの進捗率",
    },
  },
  home: {
    zeroDatasetsFound: "データセットが見つかりません",
    argillaDatasets: "データセット一覧",
    none: "データセットはありません",
    importTitle: "Hugging Face Hubからデータセットをインポート",
    importText:
      "リポジトリ名を貼り付けるだけで、Hubからデータセットをインポートできます",
    importButton: "データセットをインポート",
    importFromHub: "Hugging Faceからデータセットをインポート",
    importFromPython: "Pythonからインポート",
    importFromPythonHFWarning:
      "プライベートスペースを使用している場合は<a target='_blank' href='https://docs.argilla.io/latest/getting_started/how-to-configure-argilla-on-huggingface/#how-to-use-private-spaces'>ドキュメント</a>を参照してください。",
    exampleDatasetsTitle: "どこから始めればいいかわかりませんか？",
    exampleDatasetsText: "これらの例のデータセットを探索してみましょう",
    guidesTitle: "Argillaは初めてですか？",
    guidesText: "以下のガイドを参照してください",
    pasteRepoIdPlaceholder: "リポジトリIDを貼り付け <例> stanfordnlp/imdb",
    demoLink:
      "こちらの<a href='https://huggingface.co/spaces/argilla/argilla-template-space' target='_blank'>デモ</a>にログインしてArgillaを試してみましょう",
    name: "データセット名",
    updatedAt: "更新日",
    createdAt: "作成日",
  },
  datasetCreation: {
    questions: {
      labelSelection: {
        atLeastTwoOptions: "少なくとも2つのオプションが必要です",
        optionsWithoutLabel: "オプションを空にすることはできません",
        optionsSeparatedByComma: "ラベルはカンマ区切り",
      },
      rating: {
        atLeastTwoOptions: "少なくとも2つのオプションが必要です",
      },
      span: {
        fieldRelated: "テキストフィールドが必要です",
      },
    },
    atLeastOneQuestion: "少なくとも1つの質問が必要です",
    atLeastOneRequired: "少なくとも1つ回答必須の質問が必要です",
    hasInvalidQuestions: "無効な質問があります",
    createDataset: "Argillaにデータセットを作成",
    datasetName: "データセット名",
    name: "名前",
    assignWorkspace: "割り当てるワークスペース",
    selectSplit: "Splitを選択",
    recordWarning:
      "作成されたデータセットには最初の10K行が含まれます。以降のレコードはPython SDKで取得できます。",
    button: "データセットを作成",
    fields: "フィールド一覧",
    questionsTitle: "質問一覧",
    yourQuestions: "あなたの質問",
    requiredField: "必須フィールド",
    requiredQuestion: "質問への回答を必須にする",
    select: "選択",
    mapToColumn: "紐付けするカラム",
    applyToaAField: "範囲選択を行うフィールド",
    subset: "サブセット",
    selectSubset: "1サブセットだけでデータセットを作成できます。",
    preview: "プレビュー",
    importData: "データをインポート",
    addRecords: "レコードを追加",
    cantLoadRepository: "Hugging Faceにデータセットが見つかりません",
    none: "該当なし",
    noWorkspaces:
      "こちらの<a target='_blank' href='https://docs.argilla.io/latest/admin_guide/workspace/#create-a-new-workspace'>ガイド</a>にしたがってワークスペースを作成してください",
  },
  exportToHub: {
    dialogTitle: "Hugging Face Hubにプッシュ",
    ownerTooltip: "有効なHugging Faceのユーザー名または組織を使用してください",
    tokenTooltip: `既存のアクセストークンを使用するか、write権限付きの<a href='https://huggingface.co/settings/tokens' target='_blank'>新しいトークン</a>を作成してください`,
    validations: {
      orgOrUsernameIsRequired: "組織名またはユーザー名は必須です",
      hfTokenIsRequired: "Hugging Faceトークンは必須です",
      hfTokenInvalid: "Hugging Faceトークンが無効です",
      datasetNameIsRequired: "データセット名は必須です",
    },
    exporting: "Hugging Face Hubにエクスポート",
    private: "プライベートデータセット",
    public: "パブリックデータセット",
    exportingWarning: "これには数秒かかる場合があります",
  },
  config: {
    field: {
      text: "テキストフィールド",
      chat: "チャットフィールド",
      image: "画像フィールド",
      "no mapping": "マッピングなし",
    },
    question: {
      text: "テキスト",
      rating: "レーティング",
      label_selection: "ラベル",
      ranking: "ランキング",
      multi_label_selection: "マルチラベル",
      span: "範囲選択",
      "no mapping": "マッピングなし",
    },
    questionId: {
      text: "テキスト",
      rating: "レーティング",
      label_selection: "ラベル",
      ranking: "ランキング",
      multi_label_selection: "マルチラベル",
      span: "範囲選択",
    },
  },
  persistentStorage: {
    adminOrOwner:
      "永続ストレージが有効になっていません。このスペースが再起動されるとすべてのデータが失われます。スペース設定で有効にしてください。",
    annotator:
      "永続ストレージが有効になっていません。このスペースが再起動されるとすべてのデータが失われます。",
  },
  colorSchema: {
    system: "システム",
    light: "ライト",
    dark: "ダーク",
    "high-contrast": "高コントラスト",
  },
  validations: {
    businessLogic: {
      missing_vector: {
        message: "選択されたレコードにベクトルが見つかりません",
      },
      update_distribution_with_existing_responses: {
        message: "回答が提出されたデータセットは分配設定を変更できません。",
      },
    },
    http: {
      401: {
        message: "認証情報が正しくありません。",
      },
      404: {
        message: "リクエストされたリソースが見つかりませんでした。",
      },
      429: {
        message: "少し時間をおいてから再度お試しください。",
      },
      500: {
        message: "エラーが発生しました。時間をあけて再度お試しください。",
      },
    },
  },
  Workspaces: "ワークスペース",
};
